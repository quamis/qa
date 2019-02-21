#[allow(non_snake_case)]

fn main() {
    use crc::{crc32};

    // CRC-32-IEEE being the most commonly used one
    // assert_eq!(crc32::checksum_ieee(b"123456789"), 0xcbf43926);
    let mut data = vec!(0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, );
    println!("{}", crc32::checksum_ieee(&data));

    let data_compressed = preprocess(&mut data);
    print!("compressed to {} bytes: {:x?}", data_compressed.len(), data_compressed);
}

fn preprocess(data: &mut Vec<u8>)  -> Vec<u8> {
    let mut data_compressed: Vec<u8> = vec![];
    let mut bit_sum: Vec<u32> = vec![0;8];
    let mut running_sum: Vec<u32> = vec![0;8];
    let mut bit_list = vec![Vec::<u8>::new();8];

    for c in data.iter().enumerate() {
        println!("{:?}", c.1);
        for bp in 0..8 {
            let b = (c.1 & (1 << bp)) >> bp;
            bit_sum[bp]+= u32::from(b);

            if b!=0 {
                running_sum[bp]+= (data.len() - c.0) as u32;
            }
            
            bit_list[bp].push(b);

            println!("{} {}", bp, b); 
        }
    }

    println!("Input length: {}", data.len());
    println!("    bit sums: {}, {}, {}, {}, {}, {}, {}, {}", bit_sum[0], bit_sum[1], bit_sum[2], bit_sum[3], bit_sum[4], bit_sum[5], bit_sum[6], bit_sum[7]);
    println!("        sums: {:04x}, {:04x}, {:04x}, {:04x}, {:04x}, {:04x}, {:04x}, {:04x}", running_sum[0], running_sum[1], running_sum[2], running_sum[3], running_sum[4], running_sum[5], running_sum[6], running_sum[7]);

    // data_compressed.push(data.len());

    use byteorder::{BigEndian,WriteBytesExt};
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
