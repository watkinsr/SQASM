%{
#define _XOPEN_SOURCE 500 /* Enable certain library functions (strdup) on linux */

#include <stdio.h>     /* C declarations used in actions */
#include <stdlib.h>
#include <limits.h>
#include <string.h>
#include <Python.h>

int yylex();
void yyerror (const char *s);

/* Purely hashtable */
struct entry_s {
	char *key;
	PyObject *value;
	struct entry_s *next;
};

typedef struct entry_s entry_t;

struct hashtable_s {
	int size;
	struct entry_s **table;	
};
typedef struct hashtable_s hashtable_t;

hashtable_t *hashtable;

hashtable_t *ht_create( int size );
int ht_hash( hashtable_t *hashtable, char *key );
entry_t *ht_newpair( char *key, PyObject *value );
void ht_set( hashtable_t *hashtable, char *key, PyObject *value );
PyObject *ht_get( hashtable_t *hashtable, char *key );

/* Purely Python C-API */
char str[15]; char str2[15];

PyObject *pName, *pModule, *pDict, *pFunc, *pValue, *presult, *tup, *v, *v2;
PyObject* callpy(char* f_name, PyObject* tup);
PyObject* get_pytup(void* a1, void* a2, void* a3, char* t1, char* t2, char* t3, int n_args); 
PyObject* call_pyfunc();

int set_tupitem(char* type, void* item, int pos); 
%}

%union {int num; char* id;}         /* Yacc definitions */
%start line
%token print
%token exit_command
%token init
%token tensor
%token sel
%token measure
%token add
%token <id>gate
%token apply
%token <num> number
%token <id> identifier
%type <num> line exp term 
%type <id> assignment

%%

/* descriptions of expected inputs     corresponding actions (in C) */

line    : assignment			{;}
		| exit_command 		{exit(EXIT_SUCCESS);}
		| print exp		{printf("Printing %d\n", $2);}
		| line assignment	{;}
		| line print exp	{printf("Printing %d\n", $3);}
		| line exit_command 	{exit(EXIT_SUCCESS);}
		| line exp              {;}
		| exp		        {;}
        ;

assignment : init term term  {
	   printf("\n\n---INIT TERM TERM---\n"); 
	   tup = get_pytup($3, " ", " ", "int", NULL, NULL, 1); 
	   ht_set(hashtable, $2, callpy("INITIALIZE", tup)); 
	   ht_get( hashtable, $2 ); }
	;
exp    	: term                  {$$ = $1;}
	| exp '+' term          {$$ = $1 + $3;}
       	| exp '-' term          {$$ = $1 - $3;}
	| add term term term	{
	printf("\n\n---ADD TERM TERM TERM---\n");
	tup=get_pytup($2, $3, " ", "int", "int", " ", 2);
	ht_set(hashtable, $4, callpy("ADD", tup));
	ht_get( hashtable, $4 ); }
	| term tensor gate gate   {
	printf("\n\n--- TERM TENSOR GATE GATE ---\n"); 
	tup = get_pytup($3, $4, " ", "str", "str", NULL, 2);
	ht_set(hashtable, $1, callpy("t", tup));
	ht_get( hashtable, $1 ); }
	| term tensor term term {
	printf("\n\n--- TERM TENSOR TERM TERM ---\n");
	tup = get_pytup(ht_get(hashtable, $3), ht_get(hashtable, $4), " ", "py", "py", NULL, 2);
	ht_set(hashtable, $1, callpy("t", tup));
	ht_get( hashtable, $3 ); }
	| apply term term	{ 
	printf("\n\n--- APPLY TERM TERM ---\n"); 
	tup = get_pytup(ht_get(hashtable, $2), ht_get(hashtable, $3), " ", "py", "py", NULL, 2);
	ht_set(hashtable, $3, callpy("APPLY", tup)); 
	ht_get( hashtable, $3 ); 
	}
	| apply gate term 	{ 
	printf("\n\n--- APPLY GATE TERM ---\n"); 
	tup = get_pytup($2, ht_get(hashtable, $3), " ", "str", "py", NULL, 2); 
	ht_set(hashtable, $3, callpy("APPLY", tup));
	ht_get( hashtable, $3 );}
	| measure term term	{ 
	printf("\n\n--- MEASURE TERM TERM ---\n"); 
	tup = get_pytup(ht_get( hashtable, $2), " ", " ", "py", NULL, NULL, 1); 
	ht_set(hashtable, $3, callpy("MEASURE", tup)); 
	ht_get( hashtable, $3 ); }
	| sel term term term term { 
	printf("\n\n--- SELECT TERM TERM TERM TERM ---\n");
	printf("found args: %s, %s, %i, %i\n", $2, $3, $4, $5);
	tup = get_pytup(ht_get(hashtable, $3), $4, $5, "py", "int", "int", 3); 
	ht_set(hashtable, $2, callpy("SELECT", tup)); 
	ht_get( hashtable, $2 ); } 
	;
term   	: number                {$$ = $1;}
	| identifier		{$$ = $1;}
        ;

%%                     /* C code */


/* Create a new hashtable. */
hashtable_t *ht_create( int size ) {

	hashtable_t *hashtable = NULL;
	int i;

	if( size < 1 ) return NULL;

	/* Allocate the table itself. */
	if( ( hashtable = malloc( sizeof( hashtable_t ) ) ) == NULL ) {
		return NULL;
	}

	/* Allocate pointers to the head nodes. */
	if( ( hashtable->table = malloc( sizeof( entry_t * ) * size ) ) == NULL ) {
		return NULL;
	}
	for( i = 0; i < size; i++ ) {
		hashtable->table[i] = NULL;
	}

	hashtable->size = size;

	return hashtable;	
}

/* Hash a string for a particular hash table. */
int ht_hash( hashtable_t *hashtable, char *key ) {
	unsigned long int hashval;
	int i = 0;
	
	while( hashval < ULONG_MAX && i < strlen( key ) ) {
		hashval = hashval << 8;
		hashval += key[ i ];
		i++;
	}
	return hashval % hashtable->size;
}

/* Create a key-value pair. */
entry_t *ht_newpair( char *key, PyObject *value ) {
	entry_t *newpair;

	if( ( newpair = malloc( sizeof( entry_t ) ) ) == NULL ) {
		return NULL;
	}
	if( ( newpair->key = strdup( key ) ) == NULL ) {
		return NULL;
	}
	if( ( newpair->value = value ) == NULL ) {
		return NULL;
	}
	newpair->next = NULL;
	
	return newpair;
}

/* Insert a key-value pair into a hash table. */
void ht_set( hashtable_t *hashtable, char *key, PyObject *value ) {
	
	int bin = 0;
	entry_t *newpair = NULL;
	entry_t *next = NULL;
	entry_t *last = NULL;
	bin = ht_hash( hashtable, key );
	next = hashtable->table[ bin ];

	printf("SET HASH BIN: %i\n", bin);

	while( next != NULL && next->key != NULL && strcmp( key, next->key ) > 0 ) {
		last = next;
		next = next->next;
	}
	/* There's already a pair.  Let's replace that string. */
	if( next != NULL && next->key != NULL && strcmp( key, next->key ) == 0 ) {
		printf("Found a pair already on key: %s...\n", key);
		next->value = value;

	/* Nope, could't find it.  Time to grow a pair. */
	} else {
		newpair = ht_newpair( key, value );

		/* We're at the start of the linked list in this bin. */
		if( next == hashtable->table[ bin ] ) {
			newpair->next = next;
			hashtable->table[ bin ] = newpair;
	
		/* We're at the end of the linked list in this bin. */
		} else if ( next == NULL ) {
			last->next = newpair;
	
		/* We're in the middle of the list. */
		} else  {
			newpair->next = next;
			last->next = newpair;
		}
	}
}

/* Retrieve a key-value pair from a hash table. */
PyObject *ht_get( hashtable_t *hashtable, char *key ) {
	int bin = 0;
	entry_t *pair;
	bin = ht_hash( hashtable, key );
	printf("Trying to receive key-pair from bin: %i\n", bin);
	/* Step through the bin, looking for our value. */
	pair = hashtable->table[ bin ];
	while( pair != NULL && pair->key != NULL && strcmp( key, pair->key ) > 0 ) {
		pair = pair->next;
	}
	/* Did we actually find anything? */
	if( pair == NULL || pair->key == NULL || strcmp( key, pair->key ) != 0 ) {
		printf("ERROR: Found nothing from hashtable for key: %s\n", key);
	/* So we'll just return the key then... */
		return key;

	} else {
		printf("HASHTABLE FOUND VAL FROM KEY: %s...\n", key);
		PyObject_Print(pair->value, stdout, 0); printf("\n");
		return pair->value;
	}
	
}

PyObject* callpy(char* f_name, PyObject *tup)
{
   	pFunc = PyDict_GetItemString(pDict, (char*)f_name);
	presult = call_pyfunc();
	printf("SUCCESS: Python Simulator Function Call\n");
	return presult;
}

PyObject* get_pytup(void* a1, void* a2, void* a3, char* t1, char* t2, char* t3, int n_args) 
{
	tup = PyTuple_New(n_args);
	printf("initialised tuple with %d args...\n", n_args);
	PyErr_Print();

	if (a1 != " ") {
		set_tupitem(t1, a1, 0);
			// printf("SUCCESS set first tup item..\n");
	}
	if (a2 != " ") {
		set_tupitem(t2, a2, 1);
			// printf("SUCCESS set 2nd tup item...\n");
	}
	if (a3 != " ") {
		set_tupitem(t3, a3, 2);
			// printf("SUCCESS set third tup item...\n");
	}
	return tup;
}

int set_tupitem(char* type, void* item, int pos) {
	if (type == "py") {
		PyTuple_SetItem(tup, pos, item);
		// printf("set item[%d] as py obj\n", pos);
	}
	else if (type == "str") {
		PyTuple_SetItem(tup, pos, PyDict_GetItemString(pDict, item));
		// printf("set item[%d] as str obj\n", pos);
	}
	else if (type == "int") {
		PyTuple_SetItem(tup, pos, Py_BuildValue("i", item));
		// printf("set item[%d] as int obj\n", pos);
	}
	else {
		printf("ERROR Setting item %s in pos %d..\n", item, pos);
		return 0;
	}
	return 1;
	PyErr_Print();
}

PyObject* call_pyfunc()
{
	if (PyCallable_Check(pFunc))
   	{
		PyErr_Print();
       		printf("Trying to call Quantum Simulator...\n");
       		presult = PyObject_CallObject(pFunc,tup);
		PyErr_Print();
   	} else 
   	{
       		PyErr_Print();
   	}
	return presult;
}



int main (void) {
	/* Set PYTHONPATH TO working directory */
	setenv("PYTHONPATH",".",1);
   
 	/* Initialize the Python Interpreter */
	Py_Initialize();

	/* Prep Python */
	pName = PyString_FromString((char*)"sim");
	pModule = PyImport_Import(pName);
	pDict = PyModule_GetDict(pModule);	

	/* Init hashtable for python objects */
	hashtable = ht_create( 128 );
	
	return yyparse ( );
}

void yyerror (const char *s) {fprintf (stderr, "%s\n", s);} 

