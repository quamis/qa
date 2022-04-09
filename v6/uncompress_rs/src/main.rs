#![feature(test)]

extern crate test;

use test::Bencher;
use clap::Parser;
use itertools::Itertools;

// use rand::Rng;
use rayon::prelude::*;


// #[derive(Parser, Debug)]
// #[clap(author, version, about, long_about = None)]
// struct Args {
//     #[clap(short, long)]
//     character_table: String,
// }

fn main() {
    // let args = Args::parse();
    // println!("characterTable {}!", args.character_table);
    // let data = args.character_table.as_bytes();
    // println!("fileWithCharacterTable {:#?}!", data);


    //
    /*
     * orig text:
     *  112345678901123456789011234567890112345678901123456789011234567890112345678901123456789011234567890112345678901123456789011234567890
     * Length	132
     * CRC16	2ed1
     * CRC32	d5eb3652
     * MD5	3376a071b857b70883731e428a449b05
     * binnedLettersCompressed
     * {
     *   "missingLetter": "1",
     *   "missingCount": 24,
     *   "text": "234567890234567890234567890234567890234567890234567890234567890234567890234567890234567890234567890234567890",
     *   "length": 108
     * }
     */

    let data = "111111111111111111111111234567890234567890234567890234567890234567890234567890234567890234567890234567890234567890234567890234567890".as_bytes();
    // let data = "11123".as_bytes();

    let permutations = permute_unique_keyed(data.to_vec(), "1".as_bytes()[0]);

    println!("permutations_counter: {:?}", permutations);
}

/**
 * permutations:
 *  reset && cargo test utest_len_3_permute_unique -- --nocapture
 *  reset && cargo bench utest_len_3_permute_unique -- --nocapture
 *
 */

 /**
  * @see https://leetcode.com/problems/permutations-ii/discuss/933438/rust-heaps-algorithm
  */
fn permute_unique(mut nums: Vec<u8>) -> Vec<Vec<u8>> {
    let mut permutes = vec![];
    let n = nums.len();
    fn permute(arr: &mut Vec<u8>, size: usize, soln: &mut Vec<Vec<u8>>) {
        if size == 0 {
            soln.push(arr.clone());
        } else {
            permute(arr, size-1, soln);
            /* if size is odd swap first and last element
               if size is even swap the ith and last element */
            for i in 0..size-1 {
                if (size & 1) != 0 {
                    arr.swap(0, size-1);
                } else {
                    arr.swap(i, size-1);
                }
                permute(arr, size-1, soln);
            }
        }
    }
    permute(&mut nums, n, &mut permutes);
    permutes.sort_unstable();
    permutes.dedup();
    permutes
}

fn permute_unique_keyed(mut nums: Vec<u8>, key: u8) -> Vec<Vec<u8>> {
    let mut permutes = vec![];
    let n = nums.len();
    fn permute(arr: &mut Vec<u8>, key: u8, size: usize, soln: &mut Vec<Vec<u8>>) {
        if size == 0 {
            // println!("{:x}", md5::compute(arr.clone()));
            if format!("{:x}", md5::compute(arr.clone())) == "3376a071b857b70883731e428a449b05" {
                soln.push(arr.clone());
            }

            // soln.push(arr.clone());
        }
        else {
            permute(arr, key, size-1, soln);
            /* if size is odd swap first and last element
            if size is even swap the ith and last element */
            for i in 0..size-1 {
                if (arr[0] == key || arr[i]==key) {
                    if (size & 1) != 0 {
                        arr.swap(0, size-1);
                    }
                    else {
                        arr.swap(i, size-1);
                    }

                    permute(arr, key, size-1, soln);
                }
            }
        }
    }
    permute(&mut nums, key, n, &mut permutes);
    permutes.sort_unstable();
    permutes.dedup();
    permutes
}


// #[test]
fn utest_len_3_permute_unique() {
    let data = "123".as_bytes();

    let permutations = permute_unique(data.to_vec());

    println!("permutations_counter: {:?}", permutations);

    assert_eq!(permutations.len(), 6);
}

// #[test]
// fn utest_len_4_fike_permutations() {
//     let data = "1234".as_bytes();
//     let data_len = data.len();

//     let permutations_counter = fike_permutations_rec(&mut data.to_vec(), data_len, 0);

//     println!("permutations_counter: {:?}", permutations_counter);

//     assert_eq!(permutations_counter, 24);
// }

// /**
//  * reset && cargo bench ubench_len_4_fike_permutations
//  */

// #[bench]
// fn ubench_len_4_fike_permutations(b: &mut Bencher) {
//     let data = "1234".as_bytes();
//     let data_len = data.len();

//     println!("fileWithCharacterTable {:#?}!", data);

//     b.iter(|| fike_permutations_rec(&mut data.to_vec(), data_len, 0));
// }
