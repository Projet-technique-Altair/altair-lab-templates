#include <unistd.h>

int main(void) {
    setuid(0);
    setgid(0);
    execl("/bin/bash", "bash", "-p", "/opt/maint/run-check.sh", NULL);
    return 1;
}
