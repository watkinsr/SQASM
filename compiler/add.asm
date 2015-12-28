	extern printf		; the C function to be called ;

%macro	pabc 1			; a "simple" print macro ;
	section .data
.str	db	%1,0		; %1 is first actual in macro call ;
	section .text
        mov     rdi, fmt4	; first arg, format;
	mov	rsi, .str	; second arg ;
	mov     rdx, [a]        ; third arg ;
	mov     rcx, [b]        ; fourth arg ;
	mov     r8, [c]         ; fifth arg ; 
	mov     rax, 0	        ; no xmm used ;
	call    printf		; Call C function ;
%endmacro
	
	section .data  		; preset constants, writable ;
a:	dq	3		; 64-bit variable a initialized to 3 ;
b:	dq	4		; 64-bit variable b initializes to 4 ;
fmt4:	db "%s, a=%ld, b=%ld, c=%ld",10,0	; format string for printf ;
	
	section .bss 		; uninitialized space ; 
c:	resq	1		; reserve a 64-bit word ;

	section .text		; instructions, code segment ;
	global	 main		; for gcc standard linking ;
main:				; label ; 
	push 	rbp		; set up stack ;
	
addb:				; c=a+b ;
	mov	rax,[a]	 	; load a ;
	add	rax,[b]		; add b ;
	mov	[c],rax		; store into c ;
	pabc	"c=a+b"		; invoke the print macro ;
	ret			; main returns to operating system ;
