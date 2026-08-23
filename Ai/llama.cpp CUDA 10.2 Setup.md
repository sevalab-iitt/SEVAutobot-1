```bash
# ============================================================
# Jetson Nano — llama.cpp CUDA 10.2 Setup
# All commands + source changes made so far
# ============================================================

# ------------------------------------------------------------
# 1. External LLM drive
# ------------------------------------------------------------

sudo umount /media/jetauto/LLM
sudo mkdir -p /mnt/llm
sudo mount /dev/sda1 /mnt/llm

sudo chown -R jetauto:jetauto /mnt/llm

mkdir -p /mnt/llm/{llama.cpp,models,builds,cache,projects}

df -h /mnt/llm
lsblk -o NAME,SIZE,FSTYPE,LABEL,MOUNTPOINT,MODEL


# ------------------------------------------------------------
# 2. Permanent mount
# ------------------------------------------------------------

sudo blkid /dev/sda1

sudo nano /etc/fstab

# Add:
UUID=db6ca292-a845-4a35-bc07-e1c98503a671 /mnt/llm ext4 defaults 0 2

sudo umount /media/jetauto/LLM
sudo mkdir -p /mnt/llm
sudo mount -a

df -h /mnt/llm


# ------------------------------------------------------------
# 3. Required compiler/tool versions
# ------------------------------------------------------------

gcc-8 --version
g++-8 --version
nvcc --version
~/local_ai/cmake-3.27.1/bin/cmake --version

# Expected:
# GCC/G++ 8.4.0
# CUDA 10.2
# CMake 3.27.1


# ------------------------------------------------------------
# 4. Clone llama.cpp
# ------------------------------------------------------------

cd /mnt/llm/llama.cpp

git clone https://github.com/ggml-org/llama.cpp llama5050gpu.cpp

cd /mnt/llm/llama.cpp/llama5050gpu.cpp

git cat-file -t 23106f9

git checkout 23106f9

git checkout -b llamaJetsonNanoCUDA

git log -1 --oneline


# ------------------------------------------------------------
# 5. CUDA verification
# ------------------------------------------------------------

ls -ld /usr/local/cuda

ls /usr/local/cuda/lib64/libcudart.so*

ls -l /usr/local/cuda/include/cuda_fp16.h

find /usr/local/cuda -name 'cuda_bf16.h' -o -name 'cuda_bf16.hpp'

nvcc --version


# ------------------------------------------------------------
# 6. Initial CMake configuration
# ------------------------------------------------------------

rm -rf /mnt/llm/builds/llama.cpp

mkdir -p /mnt/llm/builds/llama.cpp

~/local_ai/cmake-3.27.1/bin/cmake \
-S /mnt/llm/llama.cpp/llama5050gpu.cpp \
-B /mnt/llm/builds/llama.cpp \
-DCMAKE_C_COMPILER=gcc-8 \
-DCMAKE_CXX_COMPILER=g++-8 \
-DGGML_CUDA=ON


# ------------------------------------------------------------
# 7. CUDA architecture compatibility
# ------------------------------------------------------------

nano CMakeLists.txt

# Added immediately after:
# project("llama.cpp" C CXX)

if(NOT DEFINED CMAKE_CUDA_ARCHITECTURES)
    set(CMAKE_CUDA_ARCHITECTURES 50 61)
endif()


# ------------------------------------------------------------
# 8. GCC linker compatibility
# ------------------------------------------------------------

nano ggml/CMakeLists.txt

# Added immediately after:
# set_target_properties(ggml PROPERTIES PUBLIC_HEADER "${GGML_PUBLIC_HEADERS}")

target_link_libraries(ggml PRIVATE stdc++fs)
add_link_options(-Wl,--copy-dt-needed-entries)


# ------------------------------------------------------------
# 9. CUDA constexpr compatibility
# ------------------------------------------------------------

nano ggml/src/ggml-cuda/common.cuh

# Changed:

static constexpr __device__ int ggml_cuda_get_physical_warp_size() {

# To:

static __device__ int ggml_cuda_get_physical_warp_size() {


# Changed:

static constexpr __device__ int8_t kvalues_iq4nl[16] = {-127, -104, -83, -65, -49, -35, -22, -10, 1, 13, 25, 38, 53, 69, 89, 113};

# To:

static __device__ int8_t kvalues_iq4nl[16] = {-127, -104, -83, -65, -49, -35, -22, -10, 1, 13, 25, 38, 53, 69, 89, 113};


# ------------------------------------------------------------
# 10. Disable __builtin_assume compatibility issue
# ------------------------------------------------------------

nano ggml/src/ggml-cuda/fattn-common.cuh

# Changed line 623:

__builtin_assume(tid < D);

# To:

// __builtin_assume(tid < D);


nano ggml/src/ggml-cuda/fattn-vec-f32.cuh

# Changed line 71:

__builtin_assume(tid < D);

# To:

// __builtin_assume(tid < D);


nano ggml/src/ggml-cuda/fattn-vec-f16.cuh

# Changed line 73:

__builtin_assume(tid < D);

# To:

// __builtin_assume(tid < D);


# ------------------------------------------------------------
# 11. Verify modifications
# ------------------------------------------------------------

grep -n "CMAKE_CUDA_ARCHITECTURES" CMakeLists.txt

grep -n -A3 -B2 "set_target_properties(ggml" ggml/CMakeLists.txt

grep -n "static.*__device__" ggml/src/ggml-cuda/common.cuh

grep -n "kvalues_iq4nl" ggml/src/ggml-cuda/common.cuh

grep -R -n "__builtin_assume" ggml/src/ggml-cuda/


# ------------------------------------------------------------
# 12. Check complete Git diff
# ------------------------------------------------------------

git status --short

git diff --check

git diff --stat

git diff -- \
CMakeLists.txt \
ggml/CMakeLists.txt \
ggml/src/ggml-cuda/common.cuh \
ggml/src/ggml-cuda/fattn-common.cuh \
ggml/src/ggml-cuda/fattn-vec-f32.cuh \
ggml/src/ggml-cuda/fattn-vec-f16.cuh


# ------------------------------------------------------------
# 13. Save compatibility patch
# ------------------------------------------------------------

git diff > /mnt/llm/projects/llamaJetsonNanoCUDA.patch

ls -lh /mnt/llm/projects/llamaJetsonNanoCUDA.patch


# ------------------------------------------------------------
# 14. Clean CMake configuration
# ------------------------------------------------------------

rm -rf /mnt/llm/builds/llama.cpp

mkdir -p /mnt/llm/builds/llama.cpp


# ------------------------------------------------------------
# 15. Configure llama.cpp for Jetson Nano CUDA 10.2
# ------------------------------------------------------------

CC=gcc-8 CXX=g++-8 \
~/local_ai/cmake-3.27.1/bin/cmake \
-S /mnt/llm/llama.cpp/llama5050gpu.cpp \
-B /mnt/llm/builds/llama.cpp \
-DCMAKE_C_COMPILER=gcc-8 \
-DCMAKE_CXX_COMPILER=g++-8 \
-DCMAKE_CUDA_HOST_COMPILER=g++-8 \
-DCMAKE_CUDA_ARCHITECTURES=53 \
-DCMAKE_CUDA_STANDARD=14 \
-DCMAKE_CUDA_STANDARD_REQUIRED=ON \
-DGGML_CUDA=ON


# ------------------------------------------------------------
# 16. Verify generated configuration
# ------------------------------------------------------------

grep -E \
"CMAKE_CUDA_ARCHITECTURES|CMAKE_CUDA_STANDARD|CMAKE_CUDA_HOST_COMPILER|CMAKE_CXX_COMPILER|GGML_CUDA" \
/mnt/llm/builds/llama.cpp/CMakeCache.txt

df -h /mnt/llm /
free -h


# ------------------------------------------------------------
# 17. Current build command
# ------------------------------------------------------------

~/local_ai/cmake-3.27.1/bin/cmake \
--build /mnt/llm/builds/llama.cpp \
--config Release \
-j1


# ------------------------------------------------------------
# 18. Useful verification commands
# ------------------------------------------------------------

git status --short

git log -1 --oneline

df -h /mnt/llm /

free -h

nvcc --version

gcc-8 --version

g++-8 --version

~/local_ai/cmake-3.27.1/bin/cmake --version
```
