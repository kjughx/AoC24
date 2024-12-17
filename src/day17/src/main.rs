extern "C" {
    fn _run(a: usize, b: usize, c: usize);
}

fn run(mut a: usize, mut b: usize, mut c: usize) -> (usize, usize, usize, usize) {
    let mut o: usize = usize::MAX;
    unsafe {
        std::arch::asm!(
            r#"
       call _run
    "#, inout("rax") a, inout("rcx") b, inout("rdx") c, out("rsi") o
        )
    };

    return (a, b, c, o)
}

fn main() {

    dbg!(run(2024, 0, 0));
}
