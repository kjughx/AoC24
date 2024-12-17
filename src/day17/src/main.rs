extern "C" {
    fn _run(a: usize, b: usize, c: usize);
}

fn run(mut a: usize, mut b: usize, mut c: usize) -> (usize, usize, usize, usize) {
    let mut o: usize = usize::MAX;
    unsafe {
        std::arch::asm!(
            r#"
       call _run
    "#, inout("r8") a, inout("r9") b, inout("r10") c, out("r11") o
        )
    };

    return (a, b, c, o)
}

fn main() {
    dbg!(run(2024, 0, 0));
}
