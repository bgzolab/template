// #include "InputBuffer.h"
#include <errno.h>
#include <fcntl.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>

#define COLUMN_USERNAME_SIZE 32
#define COLUMN_EMAIL_SIZE 255
#define TABLE_MAX_PAGES 100
/* Tree structure will limit to the size of file.*/

#define size_of_attribute(Struct, Attribute) sizeof(((Struct*)0)->Attribute) 
  /* in C, safe/pedantic calculate sizeof struct size */

typedef enum {
  NODE_INTERNAL, 
  NODE_LEAF
  }NODE_TYPE;
// Internal nodes will point to their children by storing the page number that stores the child

typedef enum {
  META_COMMAND_SUCCESS,
  META_COMMAND_UNRECOGNIZED_COMMAND
  } MetaCommandResult;

typedef enum { 
  PREPARE_SUCCESS, 
  PREPARE_NEGATIVE_ID, 
  PREPARE_STRING_TOO_LONG, 
  PREPARE_SYNTAX_ERROR, 
  PREPARE_UNRECOGNIZED_STATEMENT 
  } PrepareResult_t; /* unrecognized statement is like a expection, 
                      but not supported in C */

typedef enum {
  STATEMENT_INSERT, STATEMENT_SELECT 
  }StatementType;

typedef enum {
  EXECUTE_SUCCESS, EXECUTE_TABLE_FULL
  } ExecuteResult;

typedef struct {
  int file_descriptor;
  uint32_t file_length;
  void* pages[TABLE_MAX_PAGES];
} Pager;

typedef struct {
  Pager* pager;
  uint32_t num_rows;
} Table;

typedef struct{
  uint32_t id;
  char username[COLUMN_USERNAME_SIZE + 1];
  char email[COLUMN_EMAIL_SIZE + 1];
} Row;

typedef struct{
  StatementType type;
  Row row_to_insert;  // only used by insert statement
} Statement;

typedef struct {
  char* buffer;
  size_t buffer_length;
  ssize_t input_length;
} InputBuffer;

typedef struct {
  Table* table;
  uint32_t row_num;
  bool end_of_table;  // Indicates a position after the last element
} Cursor;

const uint32_t ID_SIZE = size_of_attribute(Row, id);
const uint32_t USERNAME_SIZE = size_of_attribute(Row, username);
const uint32_t EMAIL_SIZE = size_of_attribute(Row, email);
const uint32_t ROW_SIZE = ID_SIZE + USERNAME_SIZE + EMAIL_SIZE;

const uint32_t ID_OFFSET = 0;
const uint32_t USERNAME_OFFSET = ID_OFFSET + ID_SIZE;
const uint32_t EMAIL_OFFSET = USERNAME_OFFSET + USERNAME_SIZE;
// +----------------------------------+
// | column   | size (bytes) | offset |
// | :------- | :----------- | :----- |
// | id       | 4            | 0      |
// | username | 32           | 4      |
// | email    | 255          | 36     |
// | total    | 291          |        |
// +----------------------------------+ ???
const uint32_t PAGE_SIZE = 4096;  /* the same size as a page used in the virtual memory 
                                     systems of most computer architectures.oS will move 
                                     pages in and out of memory as whole units instead of 
                                     breaking them up*/
const uint32_t ROWS_PRE_PAGE = PAGE_SIZE / ROW_SIZE;
const uint32_t TABLE_MAX_ROWS = ROWS_PRE_PAGE * TABLE_MAX_PAGES;
// (PAGE_SIZE * TABLE_MAX_PAGES) / ROW_SIZE;

/* 
 * Common Node Header Layout Begin
 */
const uint32_t NODE_TYPE_SIZE = sizeof(uint8_t);
const uint32_t NODE_TYPE_OFFSET = 0;
const uint32_t IS_ROOT_SIZE = sizeof(uint8_t);
const uint32_t IS_ROOT_OFFSET = NODE_TYPE_SIZE;
const uint32_t PARENT_POINTER_SIZE = sizeof(uint32_t);
const uint32_t PARENT_POINTER_OFFSET = IS_ROOT_OFFSET + IS_ROOT_SIZE;
const uint8_t COMMON_NODE_HEADER_SIZE =
    NODE_TYPE_SIZE + IS_ROOT_SIZE + PARENT_POINTER_SIZE;
/* 
 * Common Node Header Layout End
 */

/* 
 * Leaf Node Header Layout Begin
 */
const uint32_t LEAF_NODE_NUM_CELLS_SIZE = sizeof(uint32_t);
const uint32_t LEAF_NODE_NUM_CELLS_OFFSET = COMMON_NODE_HEADER_SIZE;
const uint32_t LEAF_NODE_HEADER_SIZE = 
  COMMON_NODE_HEADER_SIZE + LEAF_NODE_NUM_CELLS_SIZE;
/* 
 * Leaf Node Header Layout End
 */

/*
 * Leaf Node Body Layout Begin
 */
const uint32_t LEAF_NODE_KEY_SIZE = sizeof(uint32_t);
const uint32_t LEAF_NODE_KEY_OFFSET = 0;
const uint32_t LEAF_NODE_VALUE_SIZE = ROW_SIZE;
const uint32_t LEAF_NODE_VALUE_OFFSET = 
  LEAF_NODE_KEY_OFFSET + LEAF_NODE_KEY_SIZE;
const uint32_t LEAF_NODE_CELL_SIZE = 
  LEAF_NODE_KEY_SIZE + LEAF_NODE_VALUE_SIZE;
const uint32_t LEAF_NODE_SPACE_FOR_CELLS = 
  PAGE_SIZE - LEAF_NODE_HEADER_SIZE;
const uint32_t LEAF_NODE_MAX_CELLS =
  LEAF_NODE_SPACE_FOR_CELLS / LEAF_NODE_CELL_SIZE;
/*
 * Leaf Node Body Layout End
 */

/* 
 * Accessing Leaf Node Fields Begin
 */
uint32_t* leaf_node_num_cells(void* node) {
 return node + LEAF_NODE_NUM_CELLS_OFFSET;
}

void* leaf_node_cell(void* node, uint32_t cell_num) {
  return node + LEAF_NODE_HEADER_SIZE + cell_num * LEAF_NODE_CELL_SIZE;
}
uint32_t* leaf_node_key(void* node, uint32_t cell_num) {
  return leaf_node_cell(node, cell_num);
}

void* leaf_node_value(void* node, uint32_t cell_num) {
  return leaf_node_cell(node, cell_num) + LEAF_NODE_KEY_SIZE;
}

void initialize_leaf_node(void* node) { *leaf_node_num_cells(node) = 0; }
/* 
 * Accessing Leaf Node Fields End
 */

Cursor * table_start(Table* table){
  Cursor* cursor = malloc(sizeof(Cursor));

  cursor->table = table;
  cursor->row_num = 0;
  cursor->end_of_table = (table->num_rows == 0);

  return cursor;
}

Cursor* table_end(Table* table){
  Cursor* cursor = malloc(sizeof(Cursor));

  cursor->table = table;
  cursor->row_num = table->num_rows;
  cursor->end_of_table = true;

  return cursor;
}

void cursor_advance(Cursor* cursor){
  cursor->row_num++;
  if(cursor->row_num >= cursor->table->num_rows){
    cursor->end_of_table = true;
  }
}

void print_row(Row* row) {
  printf("(%d, %s, %s)\n", row->id, row->username, row->email);
}

InputBuffer* new_input_buffer() {
  InputBuffer* input_buffer = malloc(sizeof(InputBuffer));
  input_buffer->buffer = NULL;
  input_buffer->buffer_length = 0;
  input_buffer->input_length = 0;

  return input_buffer;
}

void print_prompt() { printf("db > "); }

void read_input(InputBuffer* input_buffer) {
  ssize_t bytes_read =
      getline(&(input_buffer->buffer), &(input_buffer->buffer_length), stdin);

  if (bytes_read <= 0) {
    printf("Error reading input\n");
    exit(EXIT_FAILURE);
  }

  // Ignore trailing newline
  input_buffer->input_length = bytes_read - 1;
  input_buffer->buffer[bytes_read - 1] = 0;
}

void close_input_buffer(InputBuffer* input_buffer) {
  free(input_buffer->buffer);
  free(input_buffer);
}


void pager_flush(Pager* pager, uint32_t page_num, uint32_t size){
  
  if(pager->pages[page_num]==NULL){
    printf("Tried to flush a null page\n");
    exit(EXIT_FAILURE);
  }
  off_t offset = lseek(pager->file_descriptor, page_num * PAGE_SIZE, SEEK_SET);
  if(offset == -1){
    printf("Error seeking: %d\n", errno);
    exit(EXIT_FAILURE);
  }

  ssize_t bytes_written = 
    write(pager->file_descriptor, pager->pages[page_num], PAGE_SIZE);

  if(bytes_written == -1){
    printf("Error writing: %d\n", errno);
    exit(EXIT_FAILURE);
  }
}

void db_close(Table* table){
  Pager* pager = table->pager;
  // uint32_t num_full_pages = table->num_rows / ROWS_PRE_PAGE;

  for(uint32_t i =0;i<num_full_pages;i++){
    if(pager->pages[i] == NULL){
      continue;
    }
    pager_flush(pager, i, PAGE_SIZE);
    free(pager->pages[i]);
    pager->pages[i] = NULL;
  }
  // There may be a partial page to write to the end of the file
  // This should not be needed after we switch to a B-tree
  uint32_t num_additional_rows = table->num_rows % ROWS_PRE_PAGE;
  if(num_additional_rows > 0){
    uint32_t page_num = num_full_pages;
    pager_flush(pager, page_num, num_additional_rows * ROW_SIZE);
    free(pager->pages[page_num]);
    pager->pages[num_full_pages] = NULL;
  }

  int result = close(pager->file_descriptor);
  if(result == -1){
    printf("Error closing file: %d\n", errno);
    exit(EXIT_FAILURE);
  }
  for(uint32_t i=0; i<TABLE_MAX_PAGES; i++){
    void* page = pager->pages[i];
    if(page){
      free(page);
      pager->pages[i] = NULL;
    }
  }
  free(pager);
  free(table);
}

MetaCommandResult do_meta_command(InputBuffer* input_buffer, Table* table) {
  if(strcmp(input_buffer->buffer, ".exit") == 0){
    db_close(table);
    exit(EXIT_SUCCESS);
  } else {
    return META_COMMAND_UNRECOGNIZED_COMMAND;
  }
} // a wrapper for leaving room for more commands;

PrepareResult_t prepare_insert(InputBuffer* input_buffer, Statement* statement) {
  statement->type = STATEMENT_INSERT;

  char* keyword = strtok(input_buffer->buffer, " ");
  char* id_string = strtok(NULL, " ");
  char* username = strtok(NULL, " ");
  char* email = strtok(NULL, " ");

  if(id_string == NULL || username == NULL || email == NULL) {
    return PREPARE_SYNTAX_ERROR;
  }

  int id = atoi (id_string);
  if(id <0 ){
    return PREPARE_NEGATIVE_ID;
  }

  if(strlen(username) > COLUMN_USERNAME_SIZE) {
    return PREPARE_STRING_TOO_LONG;
  }
  
  if(strlen(email) > COLUMN_EMAIL_SIZE) {
    return PREPARE_STRING_TOO_LONG;
  }

  statement->row_to_insert.id = id;
  strcpy(statement->row_to_insert.username, username);
  strcpy(statement->row_to_insert.email, email);

  return PREPARE_SUCCESS;
}

PrepareResult_t prepare_statement(InputBuffer* input_buffer,
                                Statement* statement){
  if(strncmp(input_buffer->buffer, "insert", 6) == 0){
    return prepare_insert(input_buffer, statement);
  } // strncmp: the “insert” keyword will be followed by data.
  
  if(strcmp(input_buffer->buffer, "select") == 0){
    statement->type = STATEMENT_SELECT;
    return PREPARE_SUCCESS;
  }

  return PREPARE_UNRECOGNIZED_STATEMENT;
}


void serialize_row(Row* source, void* destination){
  memcpy(destination + ID_OFFSET, &(source->id), ID_SIZE);
  strncpy(destination + USERNAME_OFFSET, source->username, USERNAME_SIZE);
  strncpy(destination + EMAIL_OFFSET, source->email, EMAIL_SIZE);
}// convert to and from the compact representation.???

void deserialize_row(void* source, Row* destination){
  memcpy(&(destination->id), source + ID_OFFSET, ID_SIZE);
  memcpy(&(destination->username), source + USERNAME_OFFSET, USERNAME_SIZE);
  memcpy(&(destination->email), source + EMAIL_OFFSET, EMAIL_SIZE);
}// convert to and from the compact representation.???

void* get_page(Pager* pager, uint32_t page_num) {
  if( page_num>TABLE_MAX_PAGES ){
    printf("Tried to fetch page number out of bounds.%d > %d\n",
           page_num, TABLE_MAX_PAGES);
    exit(EXIT_FAILURE);
  }
  if(pager->pages[page_num] == NULL){
    // Cache miss. Allocate memory and load from disk.
    void* page = malloc(PAGE_SIZE);
    uint32_t num_pages = pager->file_length / PAGE_SIZE;

    // might have a partial page at the end.
    if(pager->file_length % PAGE_SIZE != 0){
      num_pages++;
    }

    if(page_num <= num_pages){
      // Read the page from disk.
      lseek(pager->file_descriptor, page_num * PAGE_SIZE, SEEK_SET);
      ssize_t bytes_read = read(pager->file_descriptor, page, PAGE_SIZE);
      if(bytes_read == -1){
        printf("Error reading file: %d\n", errno);
        exit(EXIT_FAILURE);
      }
    }
    pager->pages[page_num] = page;
  }

  return pager->pages[page_num];
}

void* cursor_value(Cursor* cursor){
  uint32_t row_num = cursor->row_num;
  uint32_t page_num = row_num / ROWS_PRE_PAGE;

  void* page = get_page(cursor->table->pager, page_num);

  uint32_t row_offset = row_num % ROWS_PRE_PAGE;
  uint32_t byte_offset = row_offset * ROW_SIZE;
  return page + byte_offset;
}


ExecuteResult execute_insert(Statement* statement, Table* table) {
  if(table->num_rows >= TABLE_MAX_ROWS){
    return EXECUTE_TABLE_FULL;
  }

  Row* row_to_insert = &(statement->row_to_insert);
  Cursor* cursor = table_end(table);
  serialize_row(row_to_insert, cursor_value(cursor));
  table->num_rows += 1;

  free(cursor);

  return EXECUTE_SUCCESS;
}

ExecuteResult execute_select(Statement* statement, Table* table) {
  Cursor* cursor = table_start(table);

  Row row;

  while(!(cursor->end_of_table)){
    deserialize_row(cursor_value(cursor), &row);
    print_row(&row);
    cursor_advance(cursor);
  }

  free(cursor);

  return EXECUTE_SUCCESS;
}

ExecuteResult execute_statement(Statement* statement, Table* table) {
  switch(statement->type) {
    case STATEMENT_INSERT:
      return execute_insert(statement, table);
    case STATEMENT_SELECT:
      return execute_select(statement, table);
  }
}

Pager* pager_open(const char* filename){
  int fd = open(filename, 
                O_RDWR |          // Read/Write mode
                  O_CREAT,        // Create file if it doesn't exist
                S_IWUSR |         // User write permission
                  S_IRUSR         // User read permission 0600
                );
  if (fd == -1){
    printf("Unable to open file %s\n", filename);
    exit(EXIT_FAILURE);
  }

  off_t file_length = lseek(fd, 0, SEEK_END);
  Pager* pager = malloc(sizeof(Pager));
  pager->file_descriptor = fd;
  pager->file_length = file_length;

  for(uint32_t i = 0; i<TABLE_MAX_PAGES; i++){
    pager->pages[i] = NULL;
  }

  return pager;
}

Table* db_open(const char* filename) { 
  // has the effect of opening a connection to the database
  Pager* pager = pager_open(filename);

  uint32_t num_rows = pager->file_length / ROW_SIZE;

  Table* table = (Table*)malloc(sizeof(Table));

  table->pager = pager;
  table->num_rows = num_rows;

  return table;
}


int main(int argc, char* argv[]) {

  if(argc<2){
    printf("Must supply a database filename\n");
    exit(EXIT_FAILURE);
  }

  char* filename = argv[1];
  Table* table = db_open(filename);

  InputBuffer* input_buffer = new_input_buffer();
  while (true) {
    print_prompt();
    read_input(input_buffer);

    if(input_buffer->buffer[0] == '.') {
      switch ( do_meta_command(input_buffer, table) ){
        case META_COMMAND_SUCCESS:
          continue;
        case META_COMMAND_UNRECOGNIZED_COMMAND:
          printf("Unrecognized command '%s'.\n", input_buffer->buffer);
          continue;
      }
    }

    Statement statement;
    switch ( prepare_statement(input_buffer, &statement) ){
      case PREPARE_SUCCESS:
        break;
      case PREPARE_NEGATIVE_ID:
        printf("ID must be positive.\n");
        continue;
      case PREPARE_STRING_TOO_LONG:
        printf("String is too long.\n");
        continue;
      case PREPARE_SYNTAX_ERROR:
        printf("Syntax error. Could not parse command.\n");
        continue;
      case PREPARE_UNRECOGNIZED_STATEMENT:
        printf("unrecognized keyword at start of '%s'.\n", input_buffer->buffer);
        continue;
    }

  switch (execute_statement(&statement, table)) {
    case (EXECUTE_SUCCESS):
      printf("Executed.\n");
      break;
    case (EXECUTE_TABLE_FULL):
      printf("Error: Table full.\n");
      break;
    }
  }
}