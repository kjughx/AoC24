#[inline(always)]
fn run(mut a: usize) -> (usize, usize) {
    let o;
    unsafe {
        std::arch::asm!(r#"
        push %rcx
        push %rdx
        call _run
        pop %rdx
        pop %rcx
    "#, inout("r8") a, out("rax") o, options(att_syntax))
    };

    return (a, o);
}

fn runall(mut a: usize) {
    let mut o;
    let mut v = Vec::with_capacity(64);
    loop {
        o = run(a);
        v.push(o.1);

        if o.0 == 0 {
            break;
        }
        a = o.0
    }

    println!("{v:?}");
}

fn f(aa: usize, prog: &[usize], i: usize) -> Option<usize> {
    if i == 0 {
        for a in 0..8 {
            if run((aa << 3) | a).1 == prog[0] {
                return Some((aa << 3) | a);
            }
        }

        return None;
    }

    for a in 0..8 {
        if run((aa << 3) | a).1 == prog[i] {
            let aaa = f((aa << 3) | a, prog, i - 1);
            if aaa.is_some() {
                return aaa;
            }
        }
    }

    return None;
}

fn main() {
    let input = include_str!("../program").split('\n').collect::<Vec<&str>>();
    let prog: Vec<usize> = input[4]
        .split_once(": ")
        .unwrap()
        .1
        .split(',')
        .map(|c| str::parse::<usize>(c).unwrap())
        .collect();
    let a: usize = str::parse::<usize>(input[0].split(" ").collect::<Vec<&str>>()[2]).unwrap();
    runall(a);

    let a = f(0, &prog, prog.len() - 1).unwrap();
    println!("{a}");
}
