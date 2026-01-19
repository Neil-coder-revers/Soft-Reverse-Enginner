
.intel_syntax noprefix
.global GhostUtils_GetCpuInfo

.text

# void GhostUtils_GetCpuInfo(int* info)
# RCX = pointer to int[4] buffer
GhostUtils_GetCpuInfo:
    push rbx                # Save RBX (Callee-saved in Win64 ABI)
    
    mov r8, rcx             # Save pointer arg (RCX) to R8. 
                            # CPUID clobbers EAX, EBX, ECX, EDX, so we must save the pointer.

    xor eax, eax            # Set EAX=0 (Query Vendor ID)
    cpuid                   # Exec CPUID. Out: EAX, EBX, ECX, EDX
    
    # Store results into the buffer at [R8]
    mov [r8], eax           # info[0]
    mov [r8+4], ebx         # info[1]
    mov [r8+8], ecx         # info[2]
    mov [r8+12], edx        # info[3]

    pop rbx                 # Restore RBX
    ret
