#define _GNU_SOURCE

#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <dlfcn.h>
#include <stdlib.h>

FILE* (*_fopen)(const char *path, const char *mode);
FILE* (*_fopen64)(const char *path, const char *mode);
int (*_open)(const char *pathname, int flags);
int (*_open64)(const char *pathname, int flags);

int tag_file_opened(const char *path)
{
	static const char *watched_path_prefix = NULL;
	if (watched_path_prefix == NULL) {
		watched_path_prefix = getenv("WATCHED_PATH_PREFIX");
	}
	if (strncmp(path, watched_path_prefix, strlen(watched_path_prefix)) == 0) {
		fprintf(stderr, "OPENED: %s\n", path);
		return 1;
	} else {
		return 0;
	}
}

FILE* fopen(const char *path, const char *mode)
{
	tag_file_opened(path);
    _fopen = (FILE* (*)(const char *path, const char *mode)) dlsym(RTLD_NEXT, "fopen");
    return _fopen(path, mode);
}

FILE* fopen64(const char *path, const char *mode)
{
	tag_file_opened(path);
    _fopen64 = (FILE* (*)(const char *path, const char *mode)) dlsym(RTLD_NEXT, "fopen64");
    return _fopen64(path, mode);
}

int open(const char *pathname, int flags)
{
	tag_file_opened(pathname);
	_open = (int (*)(const char *pathname, int flags)) dlsym(RTLD_NEXT, "open");
	return _open(pathname, flags);
}

int open64(const char *pathname, int flags)
{
	tag_file_opened(pathname);
	_open64 = (int (*)(const char *pathname, int flags)) dlsym(RTLD_NEXT, "open64");
	return _open64(pathname, flags);
}
