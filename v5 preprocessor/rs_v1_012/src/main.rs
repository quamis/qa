fn main() {
    use crc::{crc32};

    // CRC-32-IEEE being the most commonly used one
    // assert_eq!(crc32::checksum_ieee(b"123456789"), 0xcbf43926);
    let data = vec!(0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, );
    print!("{}", crc32::checksum_ieee(&data));

    print!("{}", preprocess(&data));
}

fn preprocess(data: &mut Vec<u8>) {
    //
}
