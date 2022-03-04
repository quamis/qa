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

/// Simple program to greet a person
#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// md5 hash to be decompressed
    #[clap(short, long)]
    md5: String,

    /// character list from where to take the characters
    #[clap(short, long)]
    fileWithCharacterTable: String,
}

fn main() {
    let args = Args::parse();

    println!("md5 {}!", args.md5);
    println!("fileWithCharacterTable {}!", args.fileWithCharacterTable);

    let data = std::fs::read(args.fileWithCharacterTable).unwrap();
    let data_len = data.len();

    println!("fileWithCharacterTable {:#?}!", data);

    // this version take up a LOP of RAM because of the .unique() call
    // for perm in data.iter().permutations(data.len()).unique() {
    // for perm in data.into_iter().permutations(data_len) {
    //     let perm_as_vec_of_chars = perm.iter().map(|b| **b as char).collect::<Vec<_>>();
    //     let perm_as_vec_of_bytes = perm.iter().map(|b| **b).collect::<Vec<_>>();
    //     let digest = md5::compute(perm_as_vec_of_bytes);
    //     // println!("try {:?}: {:?}", perm.iter().map(|b| **b as char).join(""), digest);
    //     if HEXLOWER.encode(digest.as_ref())==args.md5 {
    //         println!("found!!! {:?}: {:?}", perm_as_vec_of_chars, digest);
    //         return;
    //     }
    // }


    // works, single CPU
    // use as: cargo run -- --md5 6624a35d3fedaacec13f7af3e51b491f --file-with-character-table ./utest001-6624a35d3fedaacec13f7af3e51b491f-abac.txt
    // for perm in data.into_iter().permutations(data_len) {
    //     let perm_as_vec_of_chars = perm.iter().map(|b| *b as char).collect::<Vec<_>>();
    //     let perm_as_vec_of_bytes = perm.iter().map(|b| *b).collect::<Vec<_>>();
    //     let digest = md5::compute(perm_as_vec_of_bytes);

    //     // println!("try {:?}: {:?}", perm.iter().map(|b| **b as char).join(""), digest);
    //     if HEXLOWER.encode(digest.as_ref())==args.md5 {
    //         println!("found!!! {:?}: {:?}", perm_as_vec_of_chars, digest);
    //         return;
    //     }
    // }


    // rayon test, multi-CPUs
    let data_iterator = data.into_iter().permutations(data_len);
    let pool = rayon::ThreadPoolBuilder::new().num_threads(2).build().unwrap();
    let n = pool.install(|| permutations_scanner(data_iterator));
    println!("{}", n);


    fn permutations_scanner(mut data_iterator: itertools::Permutations<std::vec::IntoIter<u8>>) -> usize {
        let perm = data_iterator.next().unwrap();
        let perm_as_vec_of_chars = perm.iter().map(|b| *b as char).collect::<Vec<_>>();
        let perm_as_vec_of_bytes = perm.iter().map(|b| *b).collect::<Vec<_>>();
        let digest = md5::compute(perm_as_vec_of_bytes);

        println!("try {:?}: {:?}", perm.iter().map(|b| *b as char).join(""), digest);
        if HEXLOWER.encode(digest.as_ref())=="6624a35d3fedaacec13f7af3e51b491f" {
            println!("found!!! {:?}: {:?}", perm_as_vec_of_chars, digest);
            return 1;
        }
        rayon::join(|| permutations_scanner(data_iterator), || permutations_scanner(data_iterator));

        return 1;
    }



    // let result = data.into_iter().permutations(data_len)
    //     .find_first(
    //         |perm| {
    //             if rng.gen() {
    //                 return true;
    //             }
    //             else {
    //                 return false;
    //             }
    //         });

    // println!("found!!! {:?}", result);
}
