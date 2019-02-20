import time

MODULE = "DEBUG"
LEVEL = 3
DEBUG = True
LEVEL_OUTPUT = 1

__start = time.time()
def debug(string, module, level):
  if DEBUG and level <= LEVEL_OUTPUT:
    print('{:>7.3f}: {}: {}'.format(time.time()-__start, module, string))

if __name__ == "__main__":
  debug('test ok', MODULE, LEVEL)
  time.sleep(3.58)
  debug('test delay', MODULE, LEVEL)