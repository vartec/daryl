#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <dlfcn.h>
#include <stdlib.h>

FILE* (*_fopen)(const char *path, const char *mode);

int tag_file_opened(const char *path) 
{
	static const char *watched_path_prefix = NULL;
	if (watched_path_prefix == NULL) {
		watched_path_prefix = getenv("WATCHED_PATH_PREFIX");
	}
	if (strncmp(path, watched_path_prefix, strlen(watched_path_prefix)) == 0) {
		printf("%s\n", path);
		return 1;
	} else {
		return 0;
	}
}

FILE* fopen(const char *path, const char *mode)
{
    _fopen = (FILE* (*)(const char *path, const char *mode)) dlsym(RTLD_NEXT, "fopen");
    return _fopen(path, mode);
}