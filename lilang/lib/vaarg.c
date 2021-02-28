#include <stdarg.h>
#include <stdlib.h>


int vaarg(va_list ap) {
    if(ap->gp_offset < 48) {
        int result = *(int*)(ap->reg_save_area + ap->gp_offset);
        ap->gp_offset += 8;
        return result;
    } else {
        int result = *(int*)(ap->overflow_arg_area);
        ap->overflow_arg_area += 8;
        return result;
    }
}


int* vaargs(int n, va_list ap) {
    int* result = malloc(n * 8);
    for(int i = 0; i < n; i++) {
        result[i] = vaarg(ap);
    }
    return result;
}


int* vaargsint(int n, va_list ap) {
    return vaargs(n, ap);
}


int* vaargsbool(int n, va_list ap) {
    return vaargs(n, ap);
}