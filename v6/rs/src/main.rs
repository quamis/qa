use crc32fast::Hasher;
use md5::{Md5, Digest};
use std::convert::TryFrom;
use itertools::Itertools;

fn main() {
    let str = "abacabacabacabacabacabac";
    print!("Initial string: {}", str);

    // let perms = (5..8).permutations(2);
    // for e in perms {
    //     print!("{:?}", e);
    // }
}


fn myhash1(str: &[u8], _letter: u8) -> u32 {
    let mut hasher = Hasher::new();
    hasher.update(str);
    return hasher.finalize();
}

fn myhash2(str: &[u8], _letter: u8) -> [u8; 32] {
    let mut hasher = Md5::new();
    hasher.input(str);
    let result = hasher.result();
    // return result[..];
    return TryFrom::try_from(&result[0..32]).unwrap()

    // ALSO SEE https://docs.rs/xxhash-rust/0.8.2/xxhash_rust/xxh64/fn.xxh64.html
}

struct HasherResultWithStr<'a>  {
    hasherResult: HasherResultWithoutStr,
    nstr: &'a [u8],
}
struct HasherResultWithoutStr {
    letter: u8,
    strlendiff: usize,
    hash1: u32,
    hash2: [u8; 32],
    version: [u8; 2],
}

// @see https://stackoverflow.com/questions/54150353/how-to-find-and-replace-every-matching-slice-of-bytes-with-another-slice
fn remove_letter(source: &[u8], letter: u8) -> &[u8]
{
    let mut result = Vec::new();
    for i in source {
        if *i!=letter {
            result.push(i);
        }
    }

    return result.as_slice()[..];
}

fn generateHash(str: &[u8], letter: u8) -> HasherResultWithStr {
    let h: HasherResultWithStr;
    h.hasherResult.letter = letter;
    h.hasherResult.hash1 = myhash1(str, letter);
    h.hasherResult.hash2 = myhash2(str, letter);
    h.hasherResult.version = [0x00, 0x01];
    let nstr = remove_letter(str, letter);

    return h;
}