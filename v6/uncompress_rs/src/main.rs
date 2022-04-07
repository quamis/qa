#![feature(test)]

extern crate test;

use test::Bencher;
use clap::Parser;
use itertools::Itertools;

// use rand::Rng;
use rayon::prelude::*;


#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    #[clap(short, long)]
    character_table: String,
}

fn main() {
    let args = Args::parse();

    println!("characterTable {}!", args.character_table);

    let data = args.character_table.as_bytes();
    println!("fileWithCharacterTable {:#?}!", data);

}

/**
 * permutations:
 *  reset && cargo test utest_len_3_fike_permutations -- --nocapture
 *  reset && cargo bench utest_len_3_fike_permutations -- --nocapture
 *
 */
fn fike_permutations_rec(data:&mut Vec<u8>, data_len: usize, s:usize) -> u32 {
    let mut permutations_counter = 0;
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

    let permutations_counter = fike_permutations_rec(&mut data.to_vec(), data_len, 0);

    println!("permutations_counter: {:?}", permutations_counter);

    assert_eq!(permutations_counter, 6);
}

#[test]
fn utest_len_4_fike_permutations() {
    let data = "1234".as_bytes();
    let data_len = data.len();

    let permutations_counter = fike_permutations_rec(&mut data.to_vec(), data_len, 0);

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
