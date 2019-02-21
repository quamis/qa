fn main() {
    // CRC-32-IEEE being the most commonly used one
    // assert_eq!(crc32::checksum_ieee(b"123456789"), 0xcbf43926);
    let data = vec!(0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, );

    let data_compressed = preprocess(data);
    println!("compressed to {} bytes: {:x?}", data_compressed.len(), data_compressed);

    let data_uncompressed = unpreprocess(data_compressed);
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

    let mut dlen: u32 = 0;
    dlen = reader.read_u16::<BigEndian>().unwrap() as u32;

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
        bit_list[bp] = loop_call(vec![0;dlen as usize], dlen, bit_sum[bp], running_sum[bp], bit_list_crc32[bp]);
    }

    return data_uncompressed;
}

fn loop_call(mut data_uncompressed: Vec<u8>, hint_dlen: u32, hint_bit_sum: u32, hint_running_sum: u32, hint_crc32: u32) -> Vec<u8> {
    print!("{}", hint_bit_sum);
    for i in 0..hint_bit_sum {
        data_uncompressed[i as usize] = 1;        
    }

    println!("{:x?}", data_uncompressed);
    println!("rsum: {:x?}", hint_running_sum);

    return data_uncompressed;
}