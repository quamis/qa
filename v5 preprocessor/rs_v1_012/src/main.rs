fn main() {
    // CRC-32-IEEE being the most commonly used one
    // assert_eq!(crc32::checksum_ieee(b"123456789"), 0xcbf43926);
    // let data = vec!(0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, );
    let data = vec!(0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, );

    let data_compressed = preprocess(data);
    println!("compressed to {} bytes: {:x?}", data_compressed.len(), data_compressed);

    let data_uncompressed = unpreprocess(data_compressed);

    println!("uncompressed to {} bytes: {:x?}", data_uncompressed.len(), data_uncompressed);

}

fn preprocess(data: Vec<u8>)  -> Vec<u8> {
    let mut data_compressed: Vec<u8> = vec![];
    let mut bit_sum: Vec<u32> = vec![0;8];
    let mut running_sum: Vec<u32> = vec![0;8];
    let mut bit_list = vec![Vec::<u8>::new();8];

    for c in data.iter().enumerate() {
        for bp in 0..8 {
            let b = (c.1 & (1 << bp)) >> bp;
            bit_sum[bp]+= u32::from(b);

            if b!=0 {
                running_sum[bp]+= (data.len() - c.0) as u32;
            }
            
            bit_list[bp].push(b);
        }
    }

    println!("Input length: {}", data.len());
    println!("    bit sums: {}, {}, {}, {}, {}, {}, {}, {}", bit_sum[0], bit_sum[1], bit_sum[2], bit_sum[3], bit_sum[4], bit_sum[5], bit_sum[6], bit_sum[7]);
    println!("        sums: {:04x}, {:04x}, {:04x}, {:04x}, {:04x}, {:04x}, {:04x}, {:04x}", running_sum[0], running_sum[1], running_sum[2], running_sum[3], running_sum[4], running_sum[5], running_sum[6], running_sum[7]);

    // data_compressed.push(data.len());

    use byteorder::{BigEndian, WriteBytesExt};

    data_compressed.write_u16::<BigEndian>(data.len() as u16).unwrap();

    for bp in 0..8 {
        // data_compressed.push(bit_sum[bp]);
        data_compressed.write_u16::<BigEndian>(bit_sum[bp] as u16).unwrap();
    }

    for bp in 0..8 {
        // data_compressed.push(running_sum[bp]);
        data_compressed.write_u16::<BigEndian>(running_sum[bp] as u16).unwrap();
    }

    use crc::{crc32};
    for bp in 0..8 {
        // data_compressed.push(crc32::checksum_ieee(&bit_list[bp]));
        data_compressed.write_u32::<BigEndian>(crc32::checksum_ieee(&bit_list[bp])).unwrap();
    }
    

    return data_compressed;
}


fn unpreprocess(data_compressed: Vec<u8>) -> Vec<u8> {
    let mut data_uncompressed: Vec<u8> = vec![];
    let mut bit_sum: Vec<u32> = vec![0;8];
    let mut running_sum: Vec<u32> = vec![0;8];
    let mut bit_list_crc32: Vec<u32> = vec![0;8];
    let mut bit_list = vec![Vec::<u8>::new();8];
    
    use byteorder::{BigEndian, ReadBytesExt};
    use std::io::Cursor;

    let mut reader = Cursor::new(data_compressed);

    let dlen: u32 = reader.read_u16::<BigEndian>().unwrap() as u32;
    for bp in 0..8 {
        bit_sum[bp] = reader.read_u16::<BigEndian>().unwrap() as u32;
    }

    for bp in 0..8 {
        running_sum[bp] = reader.read_u16::<BigEndian>().unwrap() as u32;
    }

    for bp in 0..8 {
        bit_list_crc32[bp] = reader.read_u32::<BigEndian>().unwrap() as u32;
    }

    // re-compose the bit masks
    for bp in 0..8 {
        println!("uncompressing lane {}", bp);
        bit_list[bp] = vec![0 as u8; dlen as usize];
        let uncompressed = loop_call(&mut bit_list[bp], dlen, bit_sum[bp], running_sum[bp], bit_list_crc32[bp]);
        println!("uncompressed {:?} to {} bytes: {:x?}", uncompressed, bit_list[bp].len(), bit_list[bp]);

        unsafe {
            println!("    LOOP_CALL_REC_DBG_CALLS: {}", LOOP_CALL_REC_DBG_CALLS);
            println!("    LOOP_CALL_REC_DBG_HASHCALCULATIONS: {}", LOOP_CALL_REC_DBG_HASHCALCULATIONS);
            println!("    LOOP_CALL_REC_DBG_SHORTCIRCUIT_1: {}", LOOP_CALL_REC_DBG_SHORTCIRCUIT_1);
            println!("    LOOP_CALL_REC_DBG_SHORTCIRCUIT_2: {}", LOOP_CALL_REC_DBG_SHORTCIRCUIT_2);
            println!("    LOOP_CALL_REC_DBG_SHORTCIRCUIT_3: {}", LOOP_CALL_REC_DBG_SHORTCIRCUIT_3);
            println!("    LOOP_CALL_REC_DBG_SHORTCIRCUIT_4: {}", LOOP_CALL_REC_DBG_SHORTCIRCUIT_4);
        }

        println!("");
        if bp>1 {
            break;
        }
    }

    // TODO: re-compose data_uncompressed from bit_list

    return data_uncompressed;
}

fn loop_call(mut data_uncompressed: &mut Vec<u8>, 
                hint_dlen: u32, 
                hint_bit_sum: u32, 
                hint_rsum: u32, 
                hint_crc32: u32) -> bool {
    
    for i in 0..hint_bit_sum {
        data_uncompressed[i as usize] = 1;        
    }

    println!("hint_bit_sum: {}, data_uncompressed: {:x?}, rsum: {:x?}", hint_bit_sum, data_uncompressed, hint_rsum);

    let mut rsum = 0;
    for i in 0..hint_bit_sum {
        rsum+= (hint_dlen - i) * data_uncompressed[i as usize] as u32;
    }

    use crc::{crc32};
    let hash = crc32::checksum_ieee(&data_uncompressed);
    if hash == hint_crc32 {
        println!("found direct match: {:x?}", data_uncompressed);
        return true;
    }

    println!("    test: {:x?}", data_uncompressed);
    return loop_call_rec(&mut data_uncompressed, hint_dlen, hint_bit_sum, hint_rsum, hint_crc32, rsum, 0, hint_bit_sum);
}

static mut LOOP_CALL_REC_DBG_CALLS: u64 = 0;
static mut LOOP_CALL_REC_DBG_HASHCALCULATIONS: u64 = 0;
static mut LOOP_CALL_REC_DBG_SHORTCIRCUIT_1: u64 = 0;
static mut LOOP_CALL_REC_DBG_SHORTCIRCUIT_2: u64 = 0;
static mut LOOP_CALL_REC_DBG_SHORTCIRCUIT_3: u64 = 0;
static mut LOOP_CALL_REC_DBG_SHORTCIRCUIT_4: u64 = 0;

fn loop_call_rec(mut data_uncompressed: &mut Vec<u8>, 
                    hint_dlen: u32, 
                    hint_bit_sum: u32, 
                    hint_rsum: u32, 
                    hint_crc32: u32, 
                    mut rsum: u32, 
                    pluss: u32,
                    plusd: u32) -> bool {
    unsafe {
        LOOP_CALL_REC_DBG_CALLS+=1;
    }

    for s in ((pluss)..(hint_bit_sum)).rev() {
        if data_uncompressed[s as usize]==1 {
            if rsum < (hint_dlen - s) {
                unsafe {
                    LOOP_CALL_REC_DBG_SHORTCIRCUIT_3+=1;
                }
                break;
            }

            data_uncompressed[s as usize] = 0;
            rsum-= hint_dlen - s;

            for d in plusd..hint_dlen {
                if data_uncompressed[d as usize]==0 {
                    if rsum < (hint_dlen - d) {
                        unsafe {
                            LOOP_CALL_REC_DBG_SHORTCIRCUIT_4+=1;
                        }
                        break;
                    }

                    //if (rsum + d) > (hint_rsum + hint_rsum/2) {
                    //    break;
                    //}

                    data_uncompressed[d as usize] = 1;
                    rsum+= hint_dlen - d;

                    // print progress here
                    //println!("\r    test: {:x?}", data_uncompressed);

                    if rsum==hint_rsum { // TODO: de ce cu "or true"?
                        use crc::{crc32};
                        let hash = crc32::checksum_ieee(&data_uncompressed);
                        unsafe {
                            LOOP_CALL_REC_DBG_HASHCALCULATIONS+=1;
                        }
                        if hash == hint_crc32 {
                            return true;
                        }
                    }

                    let uncompressed = loop_call_rec(&mut data_uncompressed, hint_dlen, hint_bit_sum, hint_rsum, hint_crc32, rsum, pluss+1, d+1);
                    if uncompressed == true {
                        return uncompressed;
                    }

                    data_uncompressed[d as usize] = 0;
                    rsum-= hint_dlen - d;
                }

                if data_uncompressed[d as usize]==1 {
                    unsafe {
                        LOOP_CALL_REC_DBG_SHORTCIRCUIT_2+=1;
                    }
                    break;
                }
            }

            data_uncompressed[s as usize] = 1;
            rsum+= hint_dlen - s;
        }

        if data_uncompressed[s as usize]==0 {
            unsafe {
                LOOP_CALL_REC_DBG_SHORTCIRCUIT_1+=1;
            }
            break;
        }
    }

    return false;
}