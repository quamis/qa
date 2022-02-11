use clap::Parser;

/// Simple program to greet a person
#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Name of the person to greet
    #[clap(short, long)]
    file: String,
}

fn main() {
    let args = Args::parse();

    println!("Hello {:?}!", args.file)
}