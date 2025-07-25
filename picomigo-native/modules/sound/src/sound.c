// Include the header file to get access to the MicroPython API
#include "py/dynruntime.h"
#include "py/obj.h"

#include "rp2/sound.h"

// Helper function to compute factorial
static mp_int_t factorial_helper(mp_int_t x) {
    if (x == 0) {
        return 1;
    }
    return x * factorial_helper(x - 1);
}

// This is the function which will be called from Python, as factorial(x)
static mp_obj_t factorial(mp_obj_t x_obj) {
    // Extract the integer from the MicroPython input object
    mp_int_t x = mp_obj_get_int(x_obj);
    // Calculate the factorial
    mp_int_t result = factorial_helper(x);
    // Convert the result to a MicroPython integer object and return it
    return mp_obj_new_int(result);
}

static mp_obj_t testlist(mp_obj_t obj) {
    // void mp_obj_list_store(mp_obj_t self_in, mp_obj_t index, mp_obj_t value);
    // mp_obj_t index = mp_obj_new_int(0);
    // mp_obj_t value = mp_obj_new_int(1000);

    mp_obj_list_t *lst = MP_OBJ_TO_PTR(mp_obj_new_list(5, NULL));
    for (int i = 0; i < 5; ++i) {
        lst->items[i] = mp_obj_new_int(i);
    }
    return MP_OBJ_FROM_PTR(lst);
    // mp_obj_list_store(obj, index, value);
}

static mp_obj_t init() {
    sound_init();

    return mp_const_none;
}

// Define a Python reference to the function above
static MP_DEFINE_CONST_FUN_OBJ_1(factorial_obj, factorial);
static MP_DEFINE_CONST_FUN_OBJ_1(testlist_obj, testlist);
static MP_DEFINE_CONST_FUN_OBJ_0(init_obj, init);

// This is the entry point and is called when the module is imported
mp_obj_t
mpy_init(mp_obj_fun_bc_t *self, size_t n_args, size_t n_kw, mp_obj_t *args) {
    // This must be first, it sets up the globals dict and other things
    MP_DYNRUNTIME_INIT_ENTRY

    // Make the function available in the module's namespace
    mp_store_global(MP_QSTR_factorial, MP_OBJ_FROM_PTR(&factorial_obj));
    mp_store_global(MP_QSTR_testlist, MP_OBJ_FROM_PTR(&testlist_obj));
    mp_store_global(MP_QSTR_init, MP_OBJ_FROM_PTR(&init_obj));

    // This must be last, it restores the globals dict
    MP_DYNRUNTIME_INIT_EXIT
}
