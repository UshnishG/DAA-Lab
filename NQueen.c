#include <stdio.h>

int solve(int n, int row, int columns, int diag1, int diag2);

int totalNQueens(int n) {
    return solve(n, 0, 0, 0, 0);
}

// Recursive function with bitmasking
int solve(int n, int row, int columns, int diag1, int diag2) {
    if (row == n) {
        return 1; // All queens placed
    }

    int count = 0;
    int available = ~(columns | diag1 | diag2) & ((1 << n) - 1);

    while (available) {
        int pos = available & -available; // Rightmost available position
        available = available - pos;
        count += solve(
            n,
            row + 1,
            columns | pos,
            (diag1 | pos) << 1,
            (diag2 | pos) >> 1
        );
    }

    return count;
}

int main() {
    int n = 4; // Change this value to test other board sizes
    int result = totalNQueens(n);
    printf("Number of solutions for %d-Queens: %d\n", n, result);
    return 0;
}
