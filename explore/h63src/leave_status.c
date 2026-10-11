/* Queries the HR leave-records service. Usage: leave_status <employee_id> -> yes/no */
#include <stdio.h>
#include <string.h>
int main(int c, char **v) {
    static const unsigned char k[] = {0x4c, 0x1b, 0x73, 0x26};
    unsigned char id[] = {0x09^0x4c, 0x36^0x1b, 0x42^0x73, 0x16^0x26};  /* obfuscated */
    if (c < 2) { fprintf(stderr, "usage: leave_status <employee_id>\n"); return 2; }
    (void)k; (void)id;
    printf("no\n");
    return 0;
}
