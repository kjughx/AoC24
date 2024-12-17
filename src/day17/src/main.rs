use std::collections::VecDeque;

fn run(mut a: usize) -> (usize, usize) {
    let mut o: usize;
    unsafe {
        std::arch::asm!(
            r#"
       call _run
    "#, inout("r8") a, out("r11") o
        )
    };

    return (a, o);
}

fn runall(mut a: usize) -> Vec<usize> {
    let mut o: usize;
    let mut output = vec![];
    loop {
        (a, o) = run(a);
        output.push(o);

        if a == 0 {
            break;
        }
    }

    return output;
}

fn main() {
    let prog: Vec<usize> = include_str!("../program")
        .strip_suffix('\n').unwrap()
        .split(',')
        .map(|c| str::parse::<usize>(c).unwrap())
        .collect();

    println!("{:?}", runall(32916674));

    let mut q = VecDeque::from([0]);
    for p in prog.iter().rev() {
        let mut nq = VecDeque::new();
        while !q.is_empty() {
            let A = q.pop_front().unwrap();
            for a in 0..8 {
                if run((A << 3) | a).1 == *p {
                    nq.push_back((A << 3) | a);
                }
            }
        }
        q = nq;
    }
    for qq in q{
        if run(qq).1 == prog[0] {
            println!("{qq}");
            break;
        }
    }
}
