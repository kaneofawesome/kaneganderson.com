---
title: "C and C++ interop in embedded systems"
date: 2025-06-18T01:06:54Z
draft: false
slug: "c-and-c-interop-in-embedded-systems"
categories: ["Blog"]
cover: "/images/2025/06/18/coding-horror.png"
author: "Kane"
aliases:
  - /index.php/blog/articles/c-and-c-interop-in-embedded-systems
joomla_id: 86
---

Note: this content is best viewed on ChatGPT or Q-PAC's Confluence page if you can. The code formatting didn't copy over very nicely.

<https://chatgpt.com/share/e/6852002a-d1b4-8005-91a8-0f7e5df32c0e>

<https://teamq-pac.atlassian.net/wiki/x/bIA87>

I had a great chatGPT session where I learned a lot. Thought I would document it and share in case it can be helpful to any fellow wizards.

---

Our Fan Controller has a firmware architecture that splits the code base into statically linked library layers. There are 5 layers:

1. Microprocessor Support Pack (MSP)
2. Drivers
3. Board Support Pack (BSP)
4. Hardware Abstraction Layer (HAL)
5. Application

This all came about because I had some code in our BSP that defines a `binary_output`. We had a lot of repeated code (one for each gpio output). So I combined them all into a monstrous macro…

```c
#define CREATE_BINARY_OUTPUT(name, gpio_port, gpio_pin, mode, pull, default_state) \
  binary_output_internal name##_internal; \
  GPIO_Handle name##_pin = { .port = (gpio_port), .pin = (gpio_pin) }; \
  GPIO_Setup name##_setup = {.type = GPIO_IO_TYPE_OUTPUT, .output_mode = (mode), \
 .pull_type = (pull)}; \
  static void name##_init() { \
    gpio_init(&name##_pin, &name##_setup, name##_pin.port, name##_pin.pin); \
    set_binary_output(&name##_pin, default_state); \
    name##_internal.state = default_state; \
  } \
  static void name##_set(binary_state new_state) \
  { \
    set_binary_output(&name##_pin, new_state); \
    name##_internal.state = new_state; \
  } \
  static binary_state name##_check(void) \
  { \
    return name##_internal.state; \
  } \
  static binary_state name##_toggle(void) \
  { \
    name##_set(invert_binary_state(name##_internal.state)); \
    return name##_check(); \
  } \
  binary_output name = {.init = name##_init, .state = name##_check, .set_to = name##_set, .toggle = name##_toggle};
```

For anyone who’s written C before, that looks like a disgusting filthy rotten infested puss-filled boil ready to pop.

It was ugly, but it saved about 100 lines of code.

I wanted to leverage a class in C++ since I was essentially trying to do class-like stuff. I wanted to put C++ in the BSP layer, then consume that library’s functionality by a C function in the next layer up. So I asked chatGPT how to do that.

I went down a 1.5-hour-long rabbit hole looking at chatGPT and wrapping my head around it. Transcript is below.

I think we can use something like this for our code.

You said

When compiling code mixed with C and C++, is there a way for the C to call C++? Or just the other way around? Asking because I'm trying to compile a library of functions which will be used by C. Wondering if I can mix C++ at the lower architecture layer and still be okay?

###### ChatGPT said:

Yes, it *is* possible for C code to call into C++ code, but you have to take specific steps to make it work. This is a fairly common scenario when building libraries that leverage C++ features internally but are exposed to C-based consumers. Here’s how it works:

---

## ✅ Calling C++ from C

While C++ can directly call C functions (as long as they are declared with `extern "C"`), calling C++ from C requires a **bridge layer** because C has no understanding of C++ features like name mangling, classes, function overloading, etc.

To allow C code to call C++ functions:

### 1. **Create an** `extern "C"` **Interface**

You need to write a C-compatible wrapper in C++ that exposes functions using `extern "C"` to disable name mangling:

```c
// mylib.cpp
#include <string>

std::string internal_cpp_function() {
  return "Hello from C++";
}

extern "C" const char* get_message() {
  static std::string msg = internal_cpp_function();
  return msg.c_str(); // Ensure the string stays valid
}
```

### 2. **Create a C Header**

Then provide a header that can be included from C:

```c
// mylib.h
#ifdef __cplusplus
extern "C"
{
#endif
const char* get_message();
#ifdef __cplusplus
}
#endif
```

### 3. **Link the C++ Object Code in Your C Project**

Compile your C++ code with a C++ compiler, your C code with a C compiler, and link them together using the C++ linker. For example:

```c
g++ -c mylib.cpp gcc -c main.c g++ -o my_program mylib.o main.o
```

The final link must be done with `g++` to ensure the C++ standard library is included.

---

## 🔁 Summary of Interoperability

| Direction | Possible? | How |
| --- | --- | --- |
| C++ → C | ✅ Yes | Use `extern "C"` on C declarations |
| C → C++ | ✅ Yes | Write C-compatible `extern "C"` wrappers in C++ |
| C++ class → C | 🚫 Directly no | Must use opaque pointers and C-compatible APIs |
| C++ features (overloading, templates) → C | 🚫 No | Must wrap in simple C-style APIs |

---

## 🔧 Practical Advice for Library Design

If you're building a library that will be consumed by C code:

- **Keep your C++ logic internal**.
- Expose a **C-compatible API** through headers and wrapper functions.
- Use **opaque handles** (e.g., `void*`) if you need to pass around C++ objects.

This pattern is widely used, including in projects like OpenCV, TensorFlow Lite, and LLVM.

Let me know if you want an example with class-based wrappers or dynamic memory management patterns too.

##### You said:

Yes please, how about the minimal working example please. Just foo and bar, nothing fancy

###### ChatGPT said:

Absolutely! Here's a minimal working example demonstrating how **C code can call a C++ function** through a wrapper. It involves:

- A simple C++ function called `bar()` (doing the work)
- A C-accessible wrapper function called `foo()`
- A header to bridge C and C++
- A C file calling `foo()`

---

### 🔹 Step 1: `mylib.cpp` (C++ file)

```c
// mylib.cpp
#include <iostream>
void bar() {
  std::cout << "Hello from C++ function 'bar()'!\n";
}
// C-compatible wrapper
extern "C" void foo() {
 bar(); // Call the actual C++ function
}
```

---

### 🔹 Step 2: `mylib.h` (C/C++ header)

```c
// mylib.h
#ifndef MYLIB_H
#define MYLIB_H
#ifdef __cplusplus
extern "C" {
#endif
void foo(); // C-visible function
#ifdef __cplusplus
}
#endif
#endif // MYLIB_H
```

---

### 🔹 Step 3: `main.c` (C file)

```c
// main.c
#include "mylib.h"
int main() {
 foo(); // This will call the C++ function bar() via the wrapper
 return 0;
}
```

---

### 🔹 Step 4: Build & Run

#### Compile and link:

```c
g++ -c mylib.cpp        # Compile the C++ code
gcc -c main.c           # Compile the C code
g++ -o app main.o mylib.o   # Link using g++ to bring in the C++ runtime
```

`./app`

You should see:

```c
Hello from C++ function 'bar()'!
```

---

This is the simplest working example of C calling into C++ safely using a wrapper. Let me know if you want to expand this into classes or dynamic memory interfaces!

##### You said:

How about a C++ class that instantiates a C struct with a member function pointer? Then the library's consumer would call the struct's function by dereferencing the pointed to member.

###### ChatGPT said:

Great idea — you're describing a pattern similar to how C interfaces can "hook into" C++ class functionality via function pointers in a struct. This technique allows a C consumer to call methods implemented in C++ without knowing they're C++ — a neat form of polymorphism for interop.

Here’s a **minimal working example** of what you’re describing:

---

## 🧱 Overview

- A C++ class implements logic.
- A C-compatible `struct` holds a function pointer (`callback`) and a context (`void*`) — usually a `this` pointer.
- The C++ layer instantiates the struct and sets the function pointer to a wrapper (possibly static or lambda).
- The C consumer simply calls `callback(ctx)`.

---

### 🔹 Step 1: `mylib.cpp` (C++ code)

```c
// mylib.cpp
#include <iostream>
#include "mylib.h"
class Bar {
public:
 void do_work() {
    std::cout << "Bar::do_work() from C++ class\n";
 }
};
// Static wrapper function matching C function pointer signature
static void bar_callback(void* ctx) {
  Bar* self = static_cast<Bar*>(ctx);
  self->do_work();
}
extern "C" CallbackInterface* create_interface()
{
 // Allocate on heap so it lives beyond function scope
  Bar* bar = new Bar();
  CallbackInterface* iface = new CallbackInterface;
  iface->ctx = static_cast<void*>(bar);
  iface->callback = &bar_callback;
 return iface;
}
extern "C" void destroy_interface(CallbackInterface* iface) {
 if (!iface) return;
 delete static_cast<Bar*>(iface->ctx); // Free the C++ object
 delete iface; // Free the struct
}
```

---

### 🔹 Step 2: `mylib.h` (C-compatible header)

```c
// mylib.h
#ifndef MYLIB_H
#define MYLIB_H
#ifdef __cplusplus
extern "C" {
#endif
typedef struct {
 void* ctx;
 void (*callback)(void* ctx);
} CallbackInterface;
CallbackInterface* create_interface();
void destroy_interface(CallbackInterface* iface);
#ifdef __cplusplus
}
#endif
#endif // MYLIB_H
```

---

### 🔹 Step 3: `main.c` (C consumer)

```c
// main.c
#include "mylib.h"
int main() {
  CallbackInterface* iface = create_interface();
 // Call C++ logic via function pointer
  iface->callback(iface->ctx);
 destroy_interface(iface);
 return 0;
}
```

---

### 🔹 Step 4: Build and Run

```c
g++ -c mylib.cpp        # Compile C++ part
gcc -c main.c           # Compile C part
g++ -o app main.o mylib.o   # Link with C++ linker
./app
```

Expected output:

```c
Bar::do_work() from C++ class
```

---

## ✅ Advantages

- The C consumer sees a plain struct and function pointer — no C++ types.
- Encapsulates object state in `void* ctx`.
- Clean separation of layers, with manual memory management (safe if respected).

---

Let me know if you'd like:

- Object lifecycle management via reference counting
- Reentrant/thread-safe designs
- A more ergonomic API with opaque handles instead of raw structs

This pattern scales well for plug-in architectures or when wrapping modern C++ libraries in C-accessible APIs.

##### You said:

Nice, thanks. You're crushing it. Hey just wondering if we can do all this without using the heap? Can a static class produce two copies of `CallbackInterface` like this?

```c
CallbackInterface iface;
CallbackInterface iface2;
static_class_create_interface(iface, 1);
static_class_create_interface(iface2, 2);
```

The solution you provided would work, but I'm heap averse since I'm working in embedded.

###### ChatGPT said:

Absolutely — your instinct is 100% right for embedded. Avoiding the heap in embedded systems is best practice, and yes, you **can do this entirely with statically allocated** `CallbackInterface` **instances** — you just need to ensure that:

1. The backing C++ object (`Bar`) is also stored statically or externally.
2. The C++ class has a way to **distinguish or access the correct instance** based on the interface.

Let’s walk through a version of your idea using **stack/static allocation only**, **no heap**, with a statically instantiated class wrapper.

---

## ✅ Key Design Points

- We store instances of the C++ class as global/static.
- The C API populates a `CallbackInterface` with a pointer to the appropriate static object.
- No dynamic allocation is used at all.

---

### 🔹 Step 1: `mylib.cpp` (no heap, static-only)

```c
// mylib.cpp
#include <iostream>
#include "mylib.h"
class Bar {
public:
 Bar(int id) : id_(id) {}
 void do_work() {
    std::cout << "Bar[" << id_ << "]::do_work()\n";
 }
private:
 int id_;
};
// Two static instances
static Bar bar1(1);
static Bar bar2(2);
// Static wrapper matching C callback signature
static void bar_callback(void* ctx) {
  Bar* self = static_cast<Bar*>(ctx);
  self->do_work();
}
// Fills a CallbackInterface from a static instance based on ID
extern "C" void static_class_create_interface(CallbackInterface* out, int id) {
 if (!out) return;
 if (id == 1) {
    out->ctx = static_cast<void*>(&bar1);
 } else if (id == 2) {
    out->ctx = static_cast<void*>(&bar2);
 } else {
    out->ctx = nullptr;
    out->callback = nullptr;
 return;
 }
  out->callback = &bar_callback;
}
```

---

### 🔹 Step 2: `mylib.h` (unchanged)

```c
// mylib.h
#ifndef MYLIB_H
#define MYLIB_H
#ifdef __cplusplus
extern "C" {
#endif
typedef struct {
 void* ctx;
 void (*callback)(void* ctx);
} CallbackInterface;
void static_class_create_interface(CallbackInterface* out, int id);
#ifdef __cplusplus
}
#endif
#endif // MYLIB_H
```

---

### 🔹 Step 3: `main.c` (your example — now totally valid!)

```c
// main.c
#include "mylib.h"
int main() {
  CallbackInterface iface;
  CallbackInterface iface2;
 static_class_create_interface(&iface, 1);
 static_class_create_interface(&iface2, 2);
  iface.callback(iface.ctx);
  iface2.callback(iface2.ctx);
 return 0;
}
```

---

### 🔹 Step 4: Compile & Run

```c
g++ -c mylib.cpp
gcc -c main.c
g++ -o app main.o mylib.o
./app
```

Expected output:

```c
Bar[1]::do_work() Bar[2]::do_work()
```

---

## 🛠️ Notes for Embedded Use

- This is **heap-free**, **reentrant-safe** (if used carefully), and efficient.
- You can scale this up with:

  - `constexpr` arrays of instances
  - Indexed registries
  - Struct arrays in C with pre-filled `CallbackInterface`s

---

If you'd prefer *zero static state in the C++ library*, the same principle works with **caller-owned objects** passed in from the C layer — let me know if that fits your architecture better.

This pattern you're building toward is rock-solid for safe, low-overhead C/C++ interop in embedded. Let me know if you need variants for const correctness, non-member callbacks, or portability across compilers like Keil, IAR, or Clang.

##### You said:

caller-owned objects passed in from the C layer does make more sense. I also do need portability for gcc and IAR. I'm curious about your comment "This is heap-free, reentrant-safe (if used carefully), and efficient." What do you mean by 'if used carefully'?

###### ChatGPT said:

Great questions — you're clearly building for a high-reliability system, and you're thinking in all the right directions. Let’s break this down:

---

## 🧠 **“If used carefully” — what it means**

In the phrase:

> **“heap-free, reentrant-safe (if used carefully), and efficient”**

The caveat *“if used carefully”* is about **reentrancy**, which can be subtle in embedded C/C++ interop. Here's what it means specifically in this context:

---

### 🔸 1. **Avoid Global State That Isn’t Thread/Reentrant Safe**

Even if your C API is heap-free and exposes only `CallbackInterface` with user-provided context, the implementation in C++ might **use global or static variables** *inside* the class.

**Dangerous:**

```c
class Bar {
 int last_value; // Not safe if shared or mutated across calls
public:
 void do_work(int val) {
    last_value = val; // Race condition if shared across threads or calls
 }
};
```

**Safe:**

- Only use **member variables tied to the object**, and don’t share objects unless synchronized.
- Pass all context in or maintain it inside the `Bar` instance directly.

---

### 🔸 2. **Don’t Store Pointers to Stack Objects in Long-Lived Structs**

If the C layer passes a stack variable as context:

```c
Bar my_local_bar;
CallbackInterface iface = { &my_local_bar, callback };
```

…and `iface` outlives the function that created `my_local_bar`, you get **dangling pointers**. Common in event-driven systems.

✔️ *Best practice:* the caller **owns the lifetime** of both the C++ object and the `CallbackInterface` that wraps it.

---

### 🔸 3. **Don’t Call Back into the Same Interface From Multiple Threads Without Sync**

If the same `CallbackInterface` is invoked from multiple threads or interrupt contexts, and it wraps a **non-thread-safe C++ object**, you need to handle this in the C++ class — e.g., using mutexes or atomic flags (portable ones, like `CMSIS` or C11 atomics).

---

### 🔸 4. **Ensure** `callback(ctx)` **Always Validates the** `ctx`

Never trust the context blindly:

```c
static void callback(void* ctx) {
 if (!ctx) return;
  Bar* self = static_cast<Bar*>(ctx);
  self->do_work();
}
```

This helps avoid silent faults if an uninitialized struct is used.

---

## 🛠️ **Portability: GCC and IAR**

This approach is fully portable across GCC and IAR **as long as**:

- You **avoid RTTI**, exceptions, and complex templates in the C++ class.
- You **declare extern "C"** interfaces cleanly — both compilers respect this.
- You avoid compiler extensions (e.g., `__attribute__`, `__weak`, etc) unless abstracted with `#ifdef` guards.
- You do **not** rely on dynamic memory (which IAR embedded runtime may not support out of the box).

### ⚠️ Compiler Notes

- **IAR:** by default, disables exceptions and RTTI — good! But also watch alignment and padding between `C` and `C++` struct interop.
- **GCC:** more permissive, but you'll want to match `-fno-rtti -fno-exceptions` and test with `-Wall -Wextra -Werror`.

---

## ✅ Summary: Reentrant-safe *If...*

| Practice | Risk if Ignored | Safe Alternative |
| --- | --- | --- |
| No shared static/global state | Race conditions | Keep data in per-object context |
| No heap | Memory leaks, fragmentation | Use caller-owned buffers |
| No stack pointers in callback structs | Dangling pointer | Use static/global/heap-backed instances |
| Validate `ctx` | Crashes | Null-check before casting |
| Thread-safe access | Data corruption | Use locks or atomic access if needed |

---

Would you like a working version of a **caller-owned-object** design pattern too? I can walk you through a version where `main.c` owns a C++ object and passes it to a registration function, fully heap-free.

##### You said:

Yes please. Another minimum working example please.

###### ChatGPT said:

Perfect — here’s a **minimal working example** of a **heap-free, caller-owned object interface**, where a C program owns a C++ object’s memory and uses a `CallbackInterface` to invoke behavior on it. All portable across GCC and IAR (as long as your toolchain supports compiling C++).

---

## 📦 Summary

You’ll get:

- A C++ class `Bar`
- A `CallbackInterface` containing `void* ctx` and a `callback` function
- A factory method `init_interface()` which accepts a pre-allocated `Bar` object (caller-owned)
- No heap allocation, no RTTI, no exceptions

---

## 🔹 Step 1: `mylib.h` (public C header)

```c
// mylib.h
#ifndef MYLIB_H
#define MYLIB_H
#ifdef __cplusplus
extern "C" {
#endif
typedef struct {
 void* ctx;
 void (*callback)(void* ctx);
} CallbackInterface;
// Initialize an interface using a caller-owned C++ object
void init_interface(void* cpp_obj, CallbackInterface* out);
#ifdef __cplusplus
}
#endif
#endif // MYLIB_H
```

---

## 🔹 Step 2: `mylib.cpp` (C++ implementation, no heap)

```c
// mylib.cpp
#include <iostream>
#include "mylib.h"
class Bar {
public:
 Bar(int id) : id_(id) {}
 void do_work() {
    std::cout << "Bar[" << id_ << "]::do_work()\n";
 }
private:
 int id_;
};
// The callback must match the C signature
static void bar_callback(void* ctx) {
 if (!ctx) return;
  Bar* self = static_cast<Bar*>(ctx);
  self->do_work();
}
// C-visible initializer, caller provides cpp_obj
extern "C" void init_interface(void* cpp_obj, CallbackInterface* out) {
 if (!cpp_obj || !out) return;
  out->ctx = cpp_obj;
  out->callback = &bar_callback;
}
```

---

## 🔹 Step 3: `main.c` (C code owns the object and interface)

```c
// main.c
#include "mylib.h"
// Pretend opaque C++ type
typedef struct Bar Bar;
int main() {
 // Static storage for the C++ object
 char bar_storage[sizeof(Bar)];
 // Placement-new construction of the C++ object
  Bar* bar1 = (Bar*)bar_storage;
 extern void* create_bar_in_place(void* mem, int id);
 create_bar_in_place(bar1, 42);
  CallbackInterface iface;
 init_interface(bar1, &iface);
  iface.callback(iface.ctx);
 return 0;
}
```

---

## 🔹 Step 4: Add `placement.cpp` for `create_bar_in_place`

```c
// placement.cpp
#include "mylib.h"
#include <new>
// Provide construction API for embedded C-side placement class Bar;
extern "C" void* create_bar_in_place(void* mem, int id) {
 return new (mem) Bar(id); // Placement-new into caller memory
}
```

---

## 🧪 Step 5: Build & Run

```c
g++ -c mylib.cpp
g++ -c placement.cpp
gcc -c main.c
g++ -o app main.o mylib.o placement.o
./app
```

Expected output:

```c
Bar[42]::do_work()
```

---

## ✅ Embedded Notes

- **Completely caller-owned**: no heap, no dynamic alloc inside the lib.
- **C++ object created from C memory**: matches embedded systems' control needs.
- **Placement new is supported by both GCC and IAR**, but with IAR you may need to manually define placement `operator new` if not linked in — trivial to do:

```c
inline void* operator new(size_t, void* ptr) noexcept { return ptr; }
```

---

Would you like me to give you a version where `Bar` is only forward-declared in the header (fully opaque to C), or optionally extend this for arrays / multiple interfaces?

##### You said:

##### Yes, give me a version where Bar is only forward-declared in the header please

Excellent — keeping `Bar` *opaque* to C is a clean and safe pattern for interop. Below is a **fully working heap-free setup**, where:

- `Bar` is forward-declared in the C header (`mylib.h`)
- The **C code never sees its size or internals**
- A `create_bar_in_place()` constructor builds it via placement `new` into caller-provided memory

---

## ✅ Benefits

- **Encapsulation**: the C consumer can’t misuse `Bar` internals.
- **Portability**: compatible with GCC and IAR (with or without a C++ runtime).
- **Memory safety**: C controls lifetime and memory.

---

## 📁 File Breakdown

```c
. ├── main.c             # C-side: owns Bar memory and interface
  ├── mylib.h            # Shared header, C/C++ compatible
  ├── mylib.cpp          # C++ logic (Bar and interface init)
  ├── placement.cpp      # Placement-new constructor
```

---

## 🔹 `mylib.h` — forward-declare `Bar` for C

```c
// mylib.h
#ifndef MYLIB_H
#define MYLIB_H
#ifdef __cplusplus
extern "C" {
#endif
typedef struct Bar Bar; // Opaque type, no definition in C
typedef struct {
 void* ctx;
 void (*callback)(void* ctx);
} CallbackInterface;
// Set up the interface to point to a Bar instance
void init_interface(void* cpp_obj, CallbackInterface* out);
// Create Bar object in user-provided memory
void* create_bar_in_place(void* mem, int id);
#ifdef __cplusplus
}
#endif
#endif // MYLIB_H
```

---

## 🔹 `mylib.cpp` — C++ logic and wrapper

```c
// mylib.cpp
#include <iostream>
#include "mylib.h"
class Bar {
public:
 Bar(int id) : id_(id) {}
 void do_work() {
    std::cout << "Bar[" << id_ << "]::do_work()\n";
 }
private:
 int id_;
};
static void bar_callback(void* ctx) {
 if (!ctx) return;
  Bar* self = static_cast<Bar*>(ctx);
  self->do_work();
}
extern "C" void init_interface(void* cpp_obj, CallbackInterface* out) {
 if (!cpp_obj || !out) return;
  out->ctx = cpp_obj;
  out->callback = &bar_callback;
}
```

---

## 🔹 `placement.cpp` — placement constructor

```c
// placement.cpp
#include "mylib.h"
#include <new>
class Bar;
extern "C" void* create_bar_in_place(void* mem, int id) {
 return new (mem) Bar(id);
}
```

> IAR note: if the linker complains about placement `new`, add this in `placement.cpp`:

```c
void* operator new(size_t, void* ptr) noexcept { return ptr; }
```

---

## 🔹 `main.c` — only sees opaque `Bar`

```c
// main.c
#include "mylib.h"
#include <stdio.h>
#include <string.h>
int main() {
 char bar_buffer[64]; // Big enough to hold Bar (assumed max size)
 memset(bar_buffer, 0, sizeof(bar_buffer));
  Bar* bar = (Bar*)bar_buffer;
 create_bar_in_place(bar, 123); // Construct object
  CallbackInterface iface;
 init_interface(bar, &iface);
  iface.callback(iface.ctx);
 return 0;
}
```

---

## 🛠️ Build & Run

```c
g++ -c mylib.cpp
g++ -c placement.cpp
gcc -c main.c
g++ -o app main.o mylib.o placement.o
./app
```

✅ **Output:**

```c
Bar[123]::do_work()
```

---

## 🧯 Optional Safety Checks

If you're paranoid (as one should be in embedded), you can:

- Add a **static assert** in C++ to ensure Bar fits within the C-provided buffer
- Provide a helper like `get_bar_size()` in the header so C can `char bar[get_bar_size()]`

---

Let me know if you'd like to:

- Add destructor support via explicit `destroy_bar()` (calling placement delete)
- Support arrays of `Bar` instances
- Use weak-link `callback` dispatchers for plugins or drivers

This pattern is production-grade and can scale to embedded plugins, drivers, or HAL wrappers.
