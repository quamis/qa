use crc32fast::Hasher;
use md5::{Md5, Digest};
use std::convert::TryFrom;

fn main() {
    let str = "abacabacabacabacabacabac";
    print!("Initial string: {}", str);
}


fn myhash1(str: &[u8], _letter: u8) -> u32 {
    let mut hasher = Hasher::new();
    hasher.update(str);
    return hasher.finalize();
}

fn myhash2(str: &[u8], _letter: u8) -> [u8; 16] {
    let mut hasher = Md5::new();
    hasher.input(str);
    let result = hasher.result();
    // return result[..];
    return TryFrom::try_from(&result[0..16]).unwrap()
}


fn generateHash(str: &[u8], letter: u8)