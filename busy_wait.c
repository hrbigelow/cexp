#include <Python.h>
#include <unistd.h>
#include <time.h>

void busy_sleep(int seconds) {
    // Record the start time
    time_t start = time(NULL);
    time_t end;

    do {
        // This loop does nothing but consume CPU cycles
        for (int i = 0; i < 1000000; ++i) {
            // Volatile is used to prevent the compiler from optimizing the loop away
            asm volatile("");
        }

        // Check the elapsed time
        end = time(NULL);
    } while (difftime(end, start) < seconds);
}


static PyObject* py_busy_wait(PyObject* self, PyObject* args) {
    double wait_time;
    if (!PyArg_ParseTuple(args, "d", &wait_time)) {
        return NULL;
    }

    // Release the GIL while we 'busy wait'
    Py_BEGIN_ALLOW_THREADS
    // 'Busy wait' simulation - sleep for the given duration
    busy_sleep(wait_time);
    Py_END_ALLOW_THREADS

    Py_RETURN_NONE;
}

static PyMethodDef BusyWaitMethods[] = {
    {"busy_wait",  py_busy_wait, METH_VARARGS,
     "Perform a busy wait for a specified amount of time."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef busywaitmodule = {
    PyModuleDef_HEAD_INIT,
    "busywait",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    BusyWaitMethods
};

PyMODINIT_FUNC PyInit_busywait(void) {
    return PyModule_Create(&busywaitmodule);
}

