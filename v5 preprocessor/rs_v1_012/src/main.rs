#[allow(non_snake_case)]

fn main() {
    use crc::{crc32};

    // CRC-32-IEEE being the most commonly used one
    // assert_eq!(crc32::checksum_ieee(b"123456789"), 0xcbf43926);
    let mut data = vec!(0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, );
    println!("{}", crc32::checksum_ieee(&data));

    print!("{:?}", preprocess(&mut data));
}

fn preprocess(data: &mut Vec<u8>)  -> Vec<u8> {
    let mut data_compressed = Vec::new();
    let mut bitSum = vec![0;8];
    let mut runningSum = vec![0;8];
    let mut bitsList = vec![Vec::new();8];

    for c in data.iter().enumerate() {
        println!("{:?}", c.1);
        for bp in (0..8) {
            let b = ((c.1 & (1 << bp)) >> bp);
            bitSum[bp]+= u32::from(b);

            if b!=0 {
                runningSum[bp]+= (data.len() - c.0) as u32;
            }
            
            bitsList[bp].push(b);

            println!("{} {}", bp, b); 
        }
    }

    println!("Input length: {}", data.len());
    println!("    bit sums: {}, {}, {}, {}, {}, {}, {}, {}", bitSum[0], bitSum[1], bitSum[2], bitSum[3], bitSum[4], bitSum[5], bitSum[6], bitSum[7]);
    println!("        sums: {:04x}, {:04x}, {:04x}, {:04x}, {:04x}, {:04x}, {:04x}, {:04x}", runningSum[0], runningSum[1], runningSum[2], runningSum[3], runningSum[4], runningSum[5], runningSum[6], runningSum[7]);

    return data_compressed;
}
