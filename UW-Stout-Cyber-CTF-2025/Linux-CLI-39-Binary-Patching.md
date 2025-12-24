# Linux CLI 39: The Vault - Writeup

**Challenge Name:** Linux CLI 39: The Vault
**Points:** 400
**Category:** Reverse Engineering / Binary Patching

### Description
The challenge provides a compiled binary executable named `vault`. When you run it, it prompts you for a password. If you enter the wrong password, it prints "Access Denied." You are told that brute-forcing is impossible and hinted that you should "patch" the binary using tools like `xxd` or `sed` to bypass the check.

### Objective
Bypass the password check in the binary to reveal the flag.

### Step-by-Step Solution

#### 1. Analyze the Binary
First, verify the behavior of the program:
```bash
./vault
# Output:
# Enter Password: test
# Access Denied.

```

We need to understand the logic. Since we don't have source code, we use `objdump` to view the assembly instructions. We are looking for the `main` function where the password check likely happens.

```bash
objdump -d -M intel vault | grep -A 30 "<main>:"

```

**What to look for in the output:**

* A call to `scanf` (getting user input).
* A call to another function (likely `check_password`).
* A `test` or `cmp` instruction immediately following the function call.
* A conditional jump instruction like `je` (Jump if Equal) or `jne` (Jump if Not Equal).

*Example Output (addresses will vary):*

```assembly
1245:   call   11e9 <check_password>   ; Calls the check function
124a:   test   eax,eax                 ; Checks the result (stored in eax)
124c:   je     125f <main+0x5f>        ; Jumps if the result is 0 (False)
124e:   call   121e <decrypt_print>    ; If it didn't jump, it decrypts the flag!
1253:   jmp    126b <main+0x6b>
125f:   lea    rdi,[rip+0xdac]         ; Loads "Access Denied" string
1266:   call   1090 <puts@plt>         ; Prints "Access Denied"

```

**The Logic:**
The instruction `je 125f` means "Jump to address 125f if the previous check was 0". Address `125f` is the "Access Denied" section. We want to **stop** this jump so the program falls through to `124e` and calls `decrypt_print`.

#### 2. Find the Hex Code

We need to know the raw hexadecimal bytes for that jump instruction so we can modify them. We can use `xxd` or look closely at the full `objdump` output (if run without grep, it shows hex bytes on the left).

Standard Intel opcodes:

* `je` (Jump if Equal) is usually `74` followed by an offset.
* `jne` (Jump if Not Equal) is usually `75`.
* `nop` (No Operation) is `90`.

Let's say `objdump` showed the instruction was at offset `124c`. We can open the file in `vim` and find this specific byte sequence.

#### 3. Patching with `vim` and `xxd`

We will overwrite the `je` (Jump if Equal) with `nop` (No Operation) instructions. If we replace the jump with `nop`, the program will just slide right past the check and execute the "success" code.

1. **Open the binary in vim:**
```bash
vim -b vault

```


2. **Convert to hex view:**
Type `:%!xxd` inside vim and press Enter.
3. **Search for the instruction:**
Look for the sequence of bytes corresponding to the jump instruction found in step 1. You usually look for the bytes surrounding the call to `check_password`.
*Alternative (easier method if you just want to flip logic):*
Find the byte `74` (JE) that performs the jump and change it to `75` (JNE). This inverts the logic: "Jump if the password is WRONG" becomes "Jump if the password is RIGHT." Since the password is definitely wrong, it won't jump, and you get the flag.
*Even easier method (Noping):*
If the jump instruction is 2 bytes long (e.g., `74 15`), change both bytes to `90 90`.
4. **Edit the bytes:**
* Press `i` for insert mode.
* Change `74` to `75` (or replace bytes with `90`).
* Press `Esc`.


5. **Convert back to binary:**
Type `:%!xxd -r` inside vim and press Enter.
6. **Save and exit:**
Type `:wq` and press Enter.

#### 4. Run the Patched Binary

Now, run the modified executable.

```bash
./vault
# Output:
# Enter Password: anything
# Access Granted! Flag: STOUTCTF{...}

```

### Explanation of the Vulnerability

The program relies on client-side logic (`check_password`) to protect the secret. Since the attacker controls the binary, they can modify the instructions to bypass any logical check, regardless of how complex the password hashing algorithm is.