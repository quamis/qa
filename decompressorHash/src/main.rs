use clap::Parser;
use itertools::Itertools;
use std::fs::File;
use std::io::Read;
use std::mem;
use std::str;
use md5;
use data_encoding::HEXLOWER;

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

    println!("fileWithCharacterTable {:#?}!", data);

    for perm in data.iter().permutations(data.len()).unique() {
        let perm_as_vec_of_chars = perm.iter().map(|b| **b as char).collect::<Vec<_>>();
        let perm_as_vec_of_bytes = perm.iter().map(|b| **b).collect::<Vec<_>>();
        let digest = md5::compute(perm_as_vec_of_bytes);

        // println!("try {:?}: {:?}", perm.iter().map(|b| **b as char).join(""), digest);
        if HEXLOWER.encode(digest.as_ref())==args.md5 {
            println!("found!!! {:?}: {:?}", perm_as_vec_of_chars, digest);
            return;
        }
    }
}
