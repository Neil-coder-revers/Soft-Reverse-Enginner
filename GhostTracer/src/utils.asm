.code

; void GhostUtils_GetCpuInfo(int* info)
; RCX = pointer to int[4] buffer
GhostUtils_GetCpuInfo proc
    push rbx
    push rdx
    
    ; Execute CPUID with EAX=0
    xor rax, rax
    cpuid
    
    ; Store results in the buffer pointed to by RCX
    ; structure: [EAX, EBX, ECX, EDX]
    mov [rcx],    eax   ; info[0]
    mov [rcx+4],  ebx   ; info[1]
    mov [rcx+8],  ecx   ; info[2]
    mov [rcx+12], edx   ; info[3]

    pop rdx
    pop rbx
    ret
GhostUtils_GetCpuInfo endp

end
