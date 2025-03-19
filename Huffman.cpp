#include <iostream>
#include <algorithm>
#include <stdio.h>
using namespace std;

struct treenode {
    int freq;
    struct treenode *left;
    struct treenode *right;
};

// Comparison function for sorting in ascending order of frequency
bool compare(const treenode* a, const treenode* b) {
    return a->freq < b->freq;
}

struct treenode* CreateCode(struct treenode *s[], int no) {
    if(s[0] == NULL)
        return NULL;
    if(no == 1)
        return s[0];
    else {
        treenode* t = new treenode;
        t->left = s[0];
        t->right = s[1];
        t->freq = s[0]->freq + s[1]->freq;

        for (int i = 2; i < no; i++)
            s[i - 2] = s[i];
        s[no - 2] = t;

        // Sort array after inserting new node
        sort(s, s + no - 1, compare);

        return CreateCode(s, no - 1);
    }
}

// Print function to print all leaf nodes with 0/1 encoding
void Print(struct treenode* root, string code = "") {
    if(root == NULL)
        return;

    // If leaf node, print frequency and code
    if(root->left == NULL && root->right == NULL) {
        printf("Leaf node frequency: %d, Code: %s\n", root->freq, code.c_str());
        return;
    }

    // Traverse left with '0' added to code
    Print(root->left, code + "0");

    // Traverse right with '1' added to code
    Print(root->right, code + "1");
}

int main() {
    int n, val;
    printf("Number of frequencies:");
    scanf("%d", &n);

    struct treenode* symbols[n];

    printf("Enter frequencies:");
    for(int i = 0; i < n; i++) {
        symbols[i] = new treenode;  // Allocate memory for each node
        scanf("%d", &val);
        symbols[i]->freq = val;
        symbols[i]->left = NULL;
        symbols[i]->right = NULL;
    }

    // Sort the array of pointers based on frequency
    sort(symbols, symbols + n, compare);

    struct treenode* root = CreateCode(symbols, n);

    // Display root frequency
    printf("Root frequency: %d\n", root->freq);

    // Print all leaf nodes with their corresponding codes
    Print(root);

    // Cleanup allocated memory
    for(int i = 0; i < n; i++) {
        delete symbols[i];
    }

    return 0;
}