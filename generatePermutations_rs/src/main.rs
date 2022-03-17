#![feature(test)]

extern crate test;

use test::Bencher;
use clap::Parser;
use itertools::Itertools;
use std::fs::File;
use std::io::Read;
use std::mem;
use std::str;
use md5;
use data_encoding::HEXLOWER;

// use rand::Rng;
use rayon::prelude::*;


#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    #[clap(short, long)]
    characterTable: String,
}

/**
 * see latest nightlies for the latest version of this at https://rust-lang.github.io/rustup-components-history/
 * rustup toolchain install nightly-2022-02-23
 * rustup default nightly-2022-02-23
 *
 *
 *
 */
fn main() {
    let args = Args::parse();

    println!("characterTable {}!", args.characterTable);

    let data = args.characterTable.as_bytes();
    let data_len = data.len();

    println!("fileWithCharacterTable {:#?}!", data);

    let mut permutations_counter = 0;
    for perm in data.iter().permutations(data_len) {
        permutations_counter+=1;
        // println!("try {:?}", perm.iter().map(|b| **b as char).join(""));
    }

    println!("permutations_counter: {:?}", permutations_counter);

}


/**
 * permutations:
 *  P(n,r)
 *      n, r = 3, P = 6
 *      n, r = 4, P = 24
 *      n, r = 5, P = 120
 *      n, r = 6, P = 720
 *      n, r = 10, P = 3628800
 *      n, r = 16, P = 20922789888000
 *      n, r = 24, P = 620448401733239439360000
 *      n, r = 32, P = 263130836933693530167218012160000000
 *      n, r = 64, P = 126886932185884164103433389335161480802865516174545192198801894375214704230400000000000000
 */


fn itertools_permutations(data: &[u8], data_len: usize) -> u32 {
    let mut permutations_counter = 0;
    for perm in data.iter().permutations(data_len) {
        permutations_counter+=1;
        // println!("try {:?}", perm.iter().map(|b| **b as char).join(""));
    }

    return permutations_counter;
}


/**
 * permutations:
 *  reset && cargo test utest_len_3_fike_permutations -- --nocapture
 *  reset && cargo bench utest_len_3_fike_permutations -- --nocapture
 *
 */
fn fike_permutations_rec(data:&mut Vec<u8>, data_len: usize, s:usize) -> u32 {
    let mut permutations_counter = 0;
    let i: usize;
    if (s==data_len) {
        println!("try: {:?}", data.iter().map(|b| *b as char).join(""));
        return 1;
    }

    for i in 0..(data_len-s) {
        data.swap(s, s+i);
        permutations_counter+= fike_permutations_rec(data, data_len, s+1);
        data.swap(s, s+i);
    }

    return permutations_counter;
}


#[test]
fn utest_len_3_fike_permutations() {
    let data = "123".as_bytes();
    let data_len = data.len();

    let mut permutations_counter = fike_permutations_rec(&mut data.to_vec(), data_len, 0);

    println!("permutations_counter: {:?}", permutations_counter);

    assert_eq!(permutations_counter, 6);
}

#[test]
fn utest_len_4_fike_permutations() {
    let data = "1234".as_bytes();
    let data_len = data.len();

    let mut permutations_counter = fike_permutations_rec(&mut data.to_vec(), data_len, 0);

    println!("permutations_counter: {:?}", permutations_counter);

    assert_eq!(permutations_counter, 24);
}

/**
 * reset && cargo bench ubench_len_4_fike_permutations
 */

#[bench]
fn ubench_len_4_fike_permutations(b: &mut Bencher) {
    let data = "1234".as_bytes();
    let data_len = data.len();

    println!("fileWithCharacterTable {:#?}!", data);

    b.iter(|| fike_permutations_rec(&mut data.to_vec(), data_len, 0));
}

#[bench]
fn ubench_len_5_fike_permutations(b: &mut Bencher) {
    let data = "12345".as_bytes();
    let data_len = data.len();

    b.iter(|| fike_permutations_rec(&mut data.to_vec(), data_len, 0));
}

#[bench]
fn ubench_len_6_fike_permutations(b: &mut Bencher) {
    let data = "123456".as_bytes();
    let data_len = data.len();

    b.iter(|| fike_permutations_rec(&mut data.to_vec(), data_len, 0));
}

///////////////////////////////////////////////////////////////

#[test]
fn utest_len_3_itertools_permutations() {
    let data = "123".as_bytes();
    let data_len = data.len();

    let mut permutations_counter = itertools_permutations(data, data_len);

    println!("permutations_counter: {:?}", permutations_counter);

    assert_eq!(permutations_counter, 6);
}


#[test]
fn utest_len_4_itertools_permutations() {
    let data = "1234".as_bytes();
    let data_len = data.len();

    let mut permutations_counter = itertools_permutations(data, data_len);

    println!("permutations_counter: {:?}", permutations_counter);

    assert_eq!(permutations_counter, 24);
}


#[test]
fn utest_len_5_itertools_permutations() {
    let data = "12345".as_bytes();
    let data_len = data.len();

    let mut permutations_counter = itertools_permutations(data, data_len);

    println!("permutations_counter: {:?}", permutations_counter);

    assert_eq!(permutations_counter, 120);
}

#[test]
fn utest_len_6_itertools_permutations() {
    let data = "123456".as_bytes();
    let data_len = data.len();

    let mut permutations_counter = itertools_permutations(data, data_len);

    println!("permutations_counter: {:?}", permutations_counter);

    assert_eq!(permutations_counter, 720);
}

#[bench]
fn ubench_len_4_itertools_permutations(b: &mut Bencher) {
    let data = "1234".as_bytes();
    let data_len = data.len();

    println!("fileWithCharacterTable {:#?}!", data);

    b.iter(|| itertools_permutations(data, data_len));
}

#[bench]
fn ubench_len_5_itertools_permutations(b: &mut Bencher) {
    let data = "12345".as_bytes();
    let data_len = data.len();

    b.iter(|| itertools_permutations(data, data_len));
}

#[bench]
fn ubench_len_6_itertools_permutations(b: &mut Bencher) {
    let data = "123456".as_bytes();
    let data_len = data.len();

    b.iter(|| itertools_permutations(data, data_len));
}