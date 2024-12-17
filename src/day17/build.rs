fn main() {
    compile();

    let out_dir = std::env::var("OUT_DIR").unwrap();
    let asm_path = std::path::Path::new(&out_dir).join("prog.s");

    // Compile the assembly file
    cc::Build::new()
        .file(&asm_path) // Path to dynamically generated assembly file
        .compile("prog"); // Name of the compiled library
}

fn combo(operand: char, short: bool) -> &'static str {
    match operand {
        '0' => "$0",
        '1' => "$1",
        '2' => "$2",
        '3' => "$3",
        '4' => {
            if short {
                "%r8b"
            } else {
                "%r8"
            }
        }
        '5' => {
            if short {
                "%r9b"
            } else {
                "%r9"
            }
        }
        '6' => {
            if short {
                "%10b"
            } else {
                "%r10"
            }
        }
        _ => unreachable!("{operand}"),
    }
}

macro_rules! div {
    ($d:expr) => {
        &format!(
            r#"
        mov {}, %cl
        mov $2, %rax
        shl %cl, %rax
        mov %rax, %rcx

        mov %r8, %rax

        xor %rdx, %rdx
        div %rcx
        "#,
            $d
        )
    };
}

fn compile() {
    let prog: Vec<char> = include_str!("program")
        .split(',')
        .map(|c| c.chars().next().unwrap())
        .collect();
    let mut asm = String::from(
        r#"
    .att_syntax

    div:
        mov $2, %rdx
        shl %cl, %rdx
        mov %rdx, %rcx

        xor %rdx, %rdx
        div %rcx

        ret

    .global _run
    _run:
    "#,
    );

    for _c in prog.chunks(2) {
        let c = _c[0];
        let o = _c[1];
        asm += "nop\n";
        match c {
            '0' => {
                asm += &format!(
                    r#"
                mov %r8, %rax
                mov {}, %rcx
                call div
                mov %rax, %r8
                "#,
                    combo(o, false)
                )
            }
            '1' => {
                asm += &format!(
                    r#"
                xor ${}, %r9
                "#,
                    o
                )
            }
            '2' => {
                asm += &format!(
                    r#"
                    mov {}, %r9
                    and $7, %r9
                "#,
                    combo(o, false)
                )
            }
            '3' => {
                asm += r#"
                ret
                "#
            }
            '4' => {
                asm += r#"
                xor %r10, %r9
                "#
            }
            '5' => {
                asm += &format!(
                    r#"
                    mov {}, %r11
                "#,
                    combo(o, false)
                )
            }
            '6' => {
                asm += &format!(
                    r#"
                mov %r8, %rax
                mov {}, %rcx
                call div
                mov %rax, %r9
                "#,
                    combo(o, false)
                )
            }
            '7' => {
                asm += &format!(
                    r#"
                mov %r8, %rax
                mov {}, %rcx
                call div
                mov %rax, %r10
                "#,
                    combo(o, false)
                )
            }
            _ => unreachable!("{c}, {o}"),
        }
    }

    let out_dir = std::env::var("OUT_DIR").unwrap();
    let asm_path = std::path::Path::new(&out_dir).join("prog.s");

    // Write the assembly code to the file
    std::fs::write(&asm_path, asm).expect("Failed to write assembly file");
}
