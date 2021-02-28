#include <string.h>
#include <stdbool.h>


bool llstrcmp(char *a, char *b, char* op) {
    int comp_result = strcmp(a, b);

    if (strcmp(">", op) == 0 && comp_result > 0) return true;
    if (strcmp(">=", op) == 0 && comp_result >= 0) return true;
    if (strcmp("<", op) == 0 && comp_result < 0) return true;
    if (strcmp("<=", op) == 0 && comp_result <= 0) return true;
    if (strcmp("==", op) == 0 && comp_result == 0) return true;
    if (strcmp("!=", op) == 0 && comp_result != 0) return true;

    return false;
}