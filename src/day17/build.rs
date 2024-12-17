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
                "%al"
            } else {
                "%rax"
            }
        }
        '5' => {
            if short {
                "%cl"
            } else {
                "%rcx"
            }
        }
        '6' => {
            if short {
                "%dl"
            } else {
                "%rdx"
            }
        }
        _ => unreachable!("{operand}"),
    }
}

macro_rules! div {
    ($d:expr) => {
        &format!(
            r#"
        mov $2, %rax
        mov {}, %cl
        shl %cl, %rax
        mov %rax, %rcx

        add $16, %rsp
        pop %rax
        xor %rdx, %rdx
        div %rcx
        sub $24, %rsp
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
    .global _run
    _run:
        push %rax
        push %rcx
        push %rdx
    "#,
    );

    for _c in prog.chunks(2) {
        let c = _c[0];
        let o = _c[1];
        asm += "nop\n";
        match c {
            '0' => {
                asm += div!(combo(o, true));
                asm += r#"
                add $16, %rsp

                pop %rax
                mov %rcx, %rax
                push %rax

                sub $16, %rsp
                "#
            }
            '1' => {
                asm += &format!(
                    r#"
                add $8, %rsp
                pop %rax
                xor ${}, %rax
                push %rax
                sub $8, %rsp
                "#,
                    o
                )
            }
            '2' => {
                asm += &format!(
                    r#"
                    mov {}, %rax
                    and $7, %rax
                    add $8, %rsp
                    pop %rcx
                    mov %rax, %rcx
                    push %rcx
                    sub $8, %rsp

                "#,
                    combo(o, false)
                )
            }
            '3' => {
                asm += r#"
                pop %rdx
                pop %rcx
                pop %rax
                ret
                "#
            }
            '4' => {
                asm += r#"
                pop %rdx
                pop %rcx
                xor %rdx, %rcx
                push %rcx
                push %rdx
                "#
            }
            '5' => {
                asm += &format!(r#"
                    pop %rdx
                    pop %rcx
                    pop %rax
                    mov {}, %rsi
                    push %rax
                    push %rcx
                    push %rdx
                "#, combo(o, false))
            }
            '6' => {
                asm += div!(combo(o, true));
                asm += r#"
                    mov %rcx, %rdx
                    add $8, %rsp
                    pop %rcx
                    mov %rdx, %rcx
                    push %rcx
                    sub $8, %rsp
                "#
            }
            '7' => {
                asm += div!(combo(o, true));
                asm += r#"
                    mov %rcx, %rdx
                    pop %rcx
                    mov %rdx, %rcx
                    push %rcx
                "#
            }
            _ => unreachable!("{c}, {o}"),
        }
    }

    let out_dir = std::env::var("OUT_DIR").unwrap();
    let asm_path = std::path::Path::new(&out_dir).join("prog.s");

    // Write the assembly code to the file
    std::fs::write(&asm_path, asm).expect("Failed to write assembly file");
}
