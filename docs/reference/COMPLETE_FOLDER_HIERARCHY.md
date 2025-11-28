# COMPLETE MONOREPO FOLDER HIERARCHY - ALL FILES INCLUDED

## Root Level Files & Folders

```
├── .claude/
│   ├── commands/
│   ├── hooks/
│   └── logs/
├── .cursor/
├── .git/
│   └── hooks/
├── .github/
│   ├── actions/
│   │   └── setup-cloudflare-auth/
│   └── workflows/
├── .projects/
│   └── scripts/
├── .venv/
│   ├── bin/
│   ├── include/
│   │   └── python3.13/
│   └── lib/
│       └── python3.13/
│           └── site-packages/
│               ├── PIL/
│               │   └── .dylibs/
│               ├── _soundfile_data/
│               ├── _yaml/
│               ├── aifc/
│               ├── annotated_doc/
│               ├── annotated_types/
│               ├── anyio/
│               │   ├── _backends/
│               │   ├── _core/
│               │   ├── abc/
│               │   └── streams/
│               ├── audioop/
│               ├── audioread/
│               ├── certifi/
│               ├── cffi/
│               ├── charset_normalizer/
│               │   └── cli/
│               ├── chunk/
│               ├── click/
│               ├── cv2/
│               │   ├── .dylibs/
│               │   ├── Error/
│               │   ├── aruco/
│               │   ├── barcode/
│               │   ├── cuda/
│               │   ├── data/
│               │   ├── detail/
│               │   ├── dnn/
│               │   ├── fisheye/
│               │   ├── flann/
│               │   ├── gapi/
│               │   │   ├── core/
│               │   │   │   ├── cpu/
│               │   │   │   ├── fluid/
│               │   │   │   └── ocl/
│               │   │   ├── ie/
│               │   │   │   └── detail/
│               │   │   ├── imgproc/
│               │   │   │   └── fluid/
│               │   │   ├── oak/
│               │   │   ├── onnx/
│               │   │   │   └── ep/
│               │   │   ├── ot/
│               │   │   │   └── cpu/
│               │   │   ├── ov/
│               │   │   ├── own/
│               │   │   │   └── detail/
│               │   │   ├── render/
│               │   │   │   └── ocv/
│               │   │   ├── streaming/
│               │   │   ├── video/
│               │   │   └── wip/
│               │   │       ├── draw/
│               │   │       ├── gst/
│               │   │       └── onevpl/
│               │   ├── ipp/
│               │   ├── mat_wrapper/
│               │   ├── misc/
│               │   ├── ml/
│               │   ├── ocl/
│               │   ├── ogl/
│               │   ├── parallel/
│               │   ├── samples/
│               │   ├── segmentation/
│               │   ├── typing/
│               │   ├── utils/
│               │   │   ├── fs/
│               │   │   └── nested/
│               │   └── videoio_registry/
│               ├── dotenv/
│               ├── fastapi/
│               │   ├── _compat/
│               │   ├── dependencies/
│               │   ├── middleware/
│               │   ├── openapi/
│               │   └── security/
│               ├── h11/
│               ├── httpcore/
│               │   ├── _async/
│               │   ├── _backends/
│               │   └── _sync/
│               ├── httptools/
│               │   └── parser/
│               ├── httpx/
│               │   └── _transports/
│               ├── idna/
│               ├── imageio/
│               │   ├── config/
│               │   ├── core/
│               │   └── plugins/
│               ├── imageio_ffmpeg/
│               │   └── binaries/
│               ├── jiter/
│               ├── joblib/
│               │   ├── externals/
│               │   │   ├── cloudpickle/
│               │   │   └── loky/
│               │   │       └── backend/
│               │   └── test/
│               │       └── data/
│               ├── lazy_loader/
│               │   └── tests/
│               │       └── fake_pkg/
│               ├── librosa/
│               │   ├── core/
│               │   ├── feature/
│               │   └── util/
│               │       └── example_data/
│               ├── llvmlite/
│               │   ├── binding/
│               │   ├── ir/
│               │   └── tests/
│               ├── moviepy/
│               │   ├── audio/
│               │   │   ├── fx/
│               │   │   ├── io/
│               │   │   └── tools/
│               │   └── video/
│               │       ├── compositing/
│               │       ├── fx/
│               │       ├── io/
│               │       └── tools/
│               ├── msgpack/
│               ├── numba/
│               │   ├── cext/
│               │   ├── cloudpickle/
│               │   ├── core/
│               │   │   ├── annotations/
│               │   │   ├── datamodel/
│               │   │   ├── rewrites/
│               │   │   ├── runtime/
│               │   │   ├── typeconv/
│               │   │   ├── types/
│               │   │   ├── typing/
│               │   │   └── unsafe/
│               │   ├── cpython/
│               │   │   └── unsafe/
│               │   ├── cuda/
│               │   │   ├── cudadrv/
│               │   │   ├── kernels/
│               │   │   ├── simulator/
│               │   │   │   └── cudadrv/
│               │   │   └── tests/
│               │   │       ├── cudadrv/
│               │   │       ├── cudapy/
│               │   │       ├── cudasim/
│               │   │       ├── data/
│               │   │       ├── doc_examples/
│               │   │       │   └── ffi/
│               │   │       └── nocuda/
│               │   ├── experimental/
│               │   │   └── jitclass/
│               │   ├── misc/
│               │   │   └── help/
│               │   ├── np/
│               │   │   ├── math/
│               │   │   ├── polynomial/
│               │   │   ├── random/
│               │   │   ├── ufunc/
│               │   │   └── unsafe/
│               │   ├── parfors/
│               │   ├── pycc/
│               │   ├── scripts/
│               │   ├── stencils/
│               │   ├── testing/
│               │   ├── tests/
│               │   │   ├── doc_examples/
│               │   │   ├── gdb/
│               │   │   └── npyufunc/
│               │   ├── typed/
│               │   └── types/
│               ├── numpy/
│               │   ├── _core/
│               │   │   ├── include/
│               │   │   │   └── numpy/
│               │   │   │       └── random/
│               │   │   ├── lib/
│               │   │   │   ├── npy-pkg-config/
│               │   │   │   └── pkgconfig/
│               │   │   └── tests/
│               │   │       ├── data/
│               │   │       └── examples/
│               │   │           ├── cython/
│               │   │           └── limited_api/
│               │   ├── _pyinstaller/
│               │   │   └── tests/
│               │   ├── _typing/
│               │   ├── _utils/
│               │   ├── char/
│               │   ├── compat/
│               │   │   └── tests/
│               │   ├── core/
│               │   ├── doc/
│               │   ├── f2py/
│               │   │   ├── _backends/
│               │   │   ├── src/
│               │   │   └── tests/
│               │   │       └── src/
│               │   │           ├── abstract_interface/
│               │   │           ├── array_from_pyobj/
│               │   │           ├── assumed_shape/
│               │   │           ├── block_docstring/
│               │   │           ├── callback/
│               │   │           ├── cli/
│               │   │           ├── common/
│               │   │           ├── crackfortran/
│               │   │           ├── f2cmap/
│               │   │           ├── isocintrin/
│               │   │           ├── kind/
│               │   │           ├── mixed/
│               │   │           ├── modules/
│               │   │           │   ├── gh25337/
│               │   │           │   └── gh26920/
│               │   │           ├── negative_bounds/
│               │   │           ├── parameter/
│               │   │           ├── quoted_character/
│               │   │           ├── regression/
│               │   │           ├── return_character/
│               │   │           ├── return_complex/
│               │   │           ├── return_integer/
│               │   │           ├── return_logical/
│               │   │           ├── return_real/
│               │   │           ├── routines/
│               │   │           ├── size/
│               │   │           ├── string/
│               │   │           └── value_attrspec/
│               │   ├── fft/
│               │   │   └── tests/
│               │   ├── lib/
│               │   │   └── tests/
│               │   │       └── data/
│               │   ├── linalg/
│               │   │   └── tests/
│               │   ├── ma/
│               │   │   └── tests/
│               │   ├── matrixlib/
│               │   │   └── tests/
│               │   ├── polynomial/
│               │   │   └── tests/
│               │   ├── random/
│               │   │   ├── _examples/
│               │   │   │   ├── cffi/
│               │   │   │   ├── cython/
│               │   │   │   └── numba/
│               │   │   ├── lib/
│               │   │   └── tests/
│               │   │       └── data/
│               │   ├── rec/
│               │   ├── strings/
│               │   ├── testing/
│               │   │   ├── _private/
│               │   │   └── tests/
│               │   ├── tests/
│               │   └── typing/
│               │       └── tests/
│               │           └── data/
│               │               ├── fail/
│               │               ├── misc/
│               │               ├── pass/
│               │               └── reveal/
│               ├── openai/
│               │   ├── _extras/
│               │   ├── _utils/
│               │   ├── cli/
│               │   │   ├── _api/
│               │   │   │   ├── chat/
│               │   │   │   └── fine_tuning/
│               │   │   └── _tools/
│               │   ├── helpers/
│               │   ├── lib/
│               │   │   ├── _parsing/
│               │   │   └── streaming/
│               │   │       ├── chat/
│               │   │       └── responses/
│               │   ├── resources/
│               │   │   ├── audio/
│               │   │   ├── beta/
│               │   │   │   ├── chatkit/
│               │   │   │   ├── realtime/
│               │   │   │   └── threads/
│               │   │   │       └── runs/
│               │   │   ├── chat/
│               │   │   │   └── completions/
│               │   │   ├── containers/
│               │   │   │   └── files/
│               │   │   ├── conversations/
│               │   │   ├── evals/
│               │   │   │   └── runs/
│               │   │   ├── fine_tuning/
│               │   │   │   ├── alpha/
│               │   │   │   ├── checkpoints/
│               │   │   │   └── jobs/
│               │   │   ├── realtime/
│               │   │   ├── responses/
│               │   │   ├── uploads/
│               │   │   └── vector_stores/
│               │   └── types/
│               │       ├── audio/
│               │       ├── beta/
│               │       │   ├── chat/
│               │       │   ├── chatkit/
│               │       │   ├── realtime/
│               │       │   └── threads/
│               │       │       └── runs/
│               │       ├── chat/
│               │       │   └── completions/
│               │       ├── containers/
│               │       │   └── files/
│               │       ├── conversations/
│               │       ├── evals/
│               │       │   └── runs/
│               │       ├── fine_tuning/
│               │       │   ├── alpha/
│               │       │   ├── checkpoints/
│               │       │   └── jobs/
│               │       ├── graders/
│               │       ├── realtime/
│               │       ├── responses/
│               │       ├── shared/
│               │       ├── shared_params/
│               │       ├── uploads/
│               │       ├── vector_stores/
│               │       └── webhooks/
│               ├── packaging/
│               │   └── licenses/
│               ├── pip/
│               │   ├── _internal/
│               │   │   ├── cli/
│               │   │   ├── commands/
│               │   │   ├── index/
│               │   │   ├── locations/
│               │   │   ├── metadata/
│               │   │   │   └── importlib/
│               │   │   ├── models/
│               │   │   ├── network/
│               │   │   ├── operations/
│               │   │   │   └── install/
│               │   │   ├── req/
│               │   │   ├── resolution/
│               │   │   │   ├── legacy/
│               │   │   │   └── resolvelib/
│               │   │   ├── utils/
│               │   │   └── vcs/
│               │   └── _vendor/
│               │       ├── cachecontrol/
│               │       │   └── caches/
│               │       ├── certifi/
│               │       ├── dependency_groups/
│               │       ├── idna/
│               │       ├── msgpack/
│               │       ├── packaging/
│               │       │   └── licenses/
│               │       ├── pkg_resources/
│               │       ├── platformdirs/
│               │       ├── pygments/
│               │       │   ├── filters/
│               │       │   ├── formatters/
│               │       │   ├── lexers/
│               │       │   └── styles/
│               │       ├── pyproject_hooks/
│               │       │   └── _in_process/
│               │       ├── requests/
│               │       ├── resolvelib/
│               │       │   └── resolvers/
│               │       ├── rich/
│               │       ├── tomli/
│               │       ├── tomli_w/
│               │       ├── truststore/
│               │       └── urllib3/
│               │           ├── contrib/
│               │           │   └── _securetransport/
│               │           ├── packages/
│               │           │   └── backports/
│               │           └── util/
│               ├── pkg_resources/
│               │   └── tests/
│               │       └── data/
│               │           ├── my-test-package-source/
│               │           ├── my-test-package-zip/
│               │           ├── my-test-package_unpacked-egg/
│               │           │   └── my_test_package-1.0-py3.7.egg/
│               │           │       └── EGG-INFO/
│               │           └── my-test-package_zipped-egg/
│               ├── platformdirs/
│               ├── pooch/
│               │   └── tests/
│               │       └── data/
│               │           └── store/
│               │               └── subdir/
│               ├── proglog/
│               ├── pycparser/
│               │   └── ply/
│               ├── pydantic/
│               │   ├── _internal/
│               │   ├── deprecated/
│               │   ├── experimental/
│               │   ├── plugin/
│               │   └── v1/
│               ├── pydantic_core/
│               ├── pydantic_settings/
│               │   └── sources/
│               │       └── providers/
│               ├── requests/
│               ├── schedule/
│               ├── scipy/
│               │   ├── .dylibs/
│               │   ├── _lib/
│               │   │   ├── _uarray/
│               │   │   ├── array_api_compat/
│               │   │   │   ├── common/
│               │   │   │   ├── cupy/
│               │   │   │   ├── dask/
│               │   │   │   │   └── array/
│               │   │   │   ├── numpy/
│               │   │   │   └── torch/
│               │   │   ├── array_api_extra/
│               │   │   │   └── _lib/
│               │   │   │       └── _utils/
│               │   │   ├── cobyqa/
│               │   │   │   ├── subsolvers/
│               │   │   │   └── utils/
│               │   │   ├── pyprima/
│               │   │   │   ├── cobyla/
│               │   │   │   └── common/
│               │   │   └── tests/
│               │   ├── cluster/
│               │   │   └── tests/
│               │   ├── constants/
│               │   │   └── tests/
│               │   ├── datasets/
│               │   │   └── tests/
│               │   ├── differentiate/
│               │   │   └── tests/
│               │   ├── fft/
│               │   │   ├── _pocketfft/
│               │   │   │   └── tests/
│               │   │   └── tests/
│               │   ├── fftpack/
│               │   │   └── tests/
│               │   ├── integrate/
│               │   │   ├── _ivp/
│               │   │   │   └── tests/
│               │   │   ├── _rules/
│               │   │   └── tests/
│               │   ├── interpolate/
│               │   │   └── tests/
│               │   │       └── data/
│               │   ├── io/
│               │   │   ├── _fast_matrix_market/
│               │   │   ├── _harwell_boeing/
│               │   │   │   └── tests/
│               │   │   ├── arff/
│               │   │   │   └── tests/
│               │   │   │       └── data/
│               │   │   ├── matlab/
│               │   │   │   └── tests/
│               │   │   │       └── data/
│               │   │   └── tests/
│               │   │       └── data/
│               │   ├── linalg/
│               │   │   └── tests/
│               │   │       ├── _cython_examples/
│               │   │       └── data/
│               │   ├── misc/
│               │   ├── ndimage/
│               │   │   └── tests/
│               │   │       └── data/
│               │   ├── odr/
│               │   │   └── tests/
│               │   ├── optimize/
│               │   │   ├── _highspy/
│               │   │   ├── _lsq/
│               │   │   ├── _shgo_lib/
│               │   │   ├── _trlib/
│               │   │   ├── _trustregion_constr/
│               │   │   │   └── tests/
│               │   │   ├── cython_optimize/
│               │   │   └── tests/
│               │   │       └── _cython_examples/
│               │   ├── signal/
│               │   │   ├── tests/
│               │   │   └── windows/
│               │   ├── sparse/
│               │   │   ├── csgraph/
│               │   │   │   └── tests/
│               │   │   ├── linalg/
│               │   │   │   ├── _dsolve/
│               │   │   │   │   └── tests/
│               │   │   │   ├── _eigen/
│               │   │   │   │   ├── arpack/
│               │   │   │   │   │   └── tests/
│               │   │   │   │   ├── lobpcg/
│               │   │   │   │   │   └── tests/
│               │   │   │   │   └── tests/
│               │   │   │   ├── _isolve/
│               │   │   │   │   └── tests/
│               │   │   │   ├── _propack/
│               │   │   │   └── tests/
│               │   │   └── tests/
│               │   │       └── data/
│               │   ├── spatial/
│               │   │   ├── qhull_src/
│               │   │   ├── tests/
│               │   │   │   └── data/
│               │   │   └── transform/
│               │   │       └── tests/
│               │   ├── special/
│               │   │   ├── _precompute/
│               │   │   └── tests/
│               │   │       ├── _cython_examples/
│               │   │       └── data/
│               │   └── stats/
│               │       ├── _levy_stable/
│               │       ├── _rcont/
│               │       ├── _unuran/
│               │       └── tests/
│               │           └── data/
│               │               ├── levy_stable/
│               │               ├── nist_anova/
│               │               └── nist_linregress/
│               ├── setuptools/
│               │   ├── _vendor/
│               │   │   ├── autocommand/
│               │   │   ├── backports/
│               │   │   │   └── tarfile/
│               │   │   │       └── compat/
│               │   │   ├── importlib_metadata/
│               │   │   │   └── compat/
│               │   │   ├── inflect/
│               │   │   │   └── compat/
│               │   │   ├── jaraco/
│               │   │   │   ├── collections/
│               │   │   │   ├── functools/
│               │   │   │   └── text/
│               │   │   ├── more_itertools/
│               │   │   ├── packaging/
│               │   │   │   └── licenses/
│               │   │   ├── platformdirs/
│               │   │   ├── tomli/
│               │   │   ├── typeguard/
│               │   │   ├── wheel/
│               │   │   │   ├── cli/
│               │   │   │   └── vendored/
│               │   │   │       └── packaging/
│               │   │   └── zipp/
│               │   │       └── compat/
│               │   ├── command/
│               │   ├── compat/
│               │   ├── config/
│               │   │   └── _validate_pyproject/
│               │   └── tests/
│               │       ├── compat/
│               │       ├── config/
│               │       │   └── downloads/
│               │       ├── indexes/
│               │       │   └── test_links_priority/
│               │       │       └── simple/
│               │       │           └── foobar/
│               │       └── integration/
│               ├── sklearn/
│               │   ├── .dylibs/
│               │   ├── _loss/
│               │   │   └── tests/
│               │   ├── cluster/
│               │   │   ├── _hdbscan/
│               │   │   │   └── tests/
│               │   │   └── tests/
│               │   ├── compose/
│               │   │   └── tests/
│               │   ├── covariance/
│               │   │   └── tests/
│               │   ├── cross_decomposition/
│               │   │   └── tests/
│               │   ├── datasets/
│               │   │   ├── data/
│               │   │   ├── descr/
│               │   │   ├── images/
│               │   │   └── tests/
│               │   │       └── data/
│               │   │           └── openml/
│               │   │               ├── id_1/
│               │   │               ├── id_1119/
│               │   │               ├── id_1590/
│               │   │               ├── id_2/
│               │   │               ├── id_292/
│               │   │               ├── id_3/
│               │   │               ├── id_40589/
│               │   │               ├── id_40675/
│               │   │               ├── id_40945/
│               │   │               ├── id_40966/
│               │   │               ├── id_42074/
│               │   │               ├── id_42585/
│               │   │               ├── id_561/
│               │   │               ├── id_61/
│               │   │               └── id_62/
│               │   ├── decomposition/
│               │   │   └── tests/
│               │   ├── ensemble/
│               │   │   ├── _hist_gradient_boosting/
│               │   │   │   └── tests/
│               │   │   └── tests/
│               │   ├── experimental/
│               │   │   └── tests/
│               │   ├── externals/
│               │   │   ├── _packaging/
│               │   │   ├── _scipy/
│               │   │   │   └── sparse/
│               │   │   │       └── csgraph/
│               │   │   ├── array_api_compat/
│               │   │   │   ├── common/
│               │   │   │   ├── cupy/
│               │   │   │   ├── dask/
│               │   │   │   │   └── array/
│               │   │   │   ├── numpy/
│               │   │   │   └── torch/
│               │   │   └── array_api_extra/
│               │   │       └── _lib/
│               │   │           └── _utils/
│               │   ├── feature_extraction/
│               │   │   └── tests/
│               │   ├── feature_selection/
│               │   │   └── tests/
│               │   ├── frozen/
│               │   │   └── tests/
│               │   ├── gaussian_process/
│               │   │   └── tests/
│               │   ├── impute/
│               │   │   └── tests/
│               │   ├── inspection/
│               │   │   ├── _plot/
│               │   │   │   └── tests/
│               │   │   └── tests/
│               │   ├── linear_model/
│               │   │   ├── _glm/
│               │   │   │   └── tests/
│               │   │   └── tests/
│               │   ├── manifold/
│               │   │   └── tests/
│               │   ├── metrics/
│               │   │   ├── _plot/
│               │   │   │   └── tests/
│               │   │   ├── cluster/
│               │   │   │   └── tests/
│               │   │   └── tests/
│               │   ├── mixture/
│               │   │   └── tests/
│               │   ├── model_selection/
│               │   │   └── tests/
│               │   ├── neighbors/
│               │   │   └── tests/
│               │   ├── neural_network/
│               │   │   └── tests/
│               │   ├── preprocessing/
│               │   │   └── tests/
│               │   ├── semi_supervised/
│               │   │   └── tests/
│               │   ├── svm/
│               │   │   ├── src/
│               │   │   │   ├── liblinear/
│               │   │   │   ├── libsvm/
│               │   │   │   └── newrand/
│               │   │   └── tests/
│               │   ├── tests/
│               │   ├── tree/
│               │   │   └── tests/
│               │   └── utils/
│               │       ├── _repr_html/
│               │       │   └── tests/
│               │       ├── _test_common/
│               │       ├── src/
│               │       └── tests/
│               ├── sniffio/
│               │   └── _tests/
│               ├── soxr/
│               ├── sqlalchemy/
│               │   ├── connectors/
│               │   ├── cyextension/
│               │   ├── dialects/
│               │   │   ├── mssql/
│               │   │   ├── mysql/
│               │   │   ├── oracle/
│               │   │   ├── postgresql/
│               │   │   └── sqlite/
│               │   ├── engine/
│               │   ├── event/
│               │   ├── ext/
│               │   │   ├── asyncio/
│               │   │   ├── declarative/
│               │   │   └── mypy/
│               │   ├── future/
│               │   ├── orm/
│               │   ├── pool/
│               │   ├── sql/
│               │   ├── testing/
│               │   │   ├── fixtures/
│               │   │   ├── plugin/
│               │   │   └── suite/
│               │   └── util/
│               ├── starlette/
│               │   └── middleware/
│               ├── sunau/
│               ├── tqdm/
│               │   └── contrib/
│               ├── typing_inspection/
│               ├── urllib3/
│               │   ├── contrib/
│               │   │   └── emscripten/
│               │   ├── http2/
│               │   └── util/
│               ├── uvicorn/
│               │   ├── lifespan/
│               │   ├── loops/
│               │   ├── middleware/
│               │   ├── protocols/
│               │   │   ├── http/
│               │   │   └── websockets/
│               │   └── supervisors/
│               ├── uvloop/
│               │   ├── handles/
│               │   └── includes/
│               ├── watchfiles/
│               ├── websockets/
│               │   ├── asyncio/
│               │   ├── extensions/
│               │   ├── legacy/
│               │   └── sync/
│               ├── wheel/
│               │   ├── cli/
│               │   └── vendored/
│               │       └── packaging/
│               └── yaml/
├── .vscode/
├── AIGuards-Backend/
│   ├── .claude/
│   ├── .cursor/
│   │   └── rules/
│   ├── .git/
│   │   ├── hooks/
│   │   ├── info/
│   │   ├── logs/
│   │   │   └── refs/
│   │   │       ├── heads/
│   │   │       └── remotes/
│   │   │           └── origin/
│   │   ├── objects/
│   │   │   ├── 03/
│   │   │   ├── 0e/
│   │   │   ├── 0f/
│   │   │   ├── 10/
│   │   │   ├── 1a/
│   │   │   ├── 1c/
│   │   │   ├── 20/
│   │   │   ├── 22/
│   │   │   ├── 25/
│   │   │   ├── 28/
│   │   │   ├── 2b/
│   │   │   ├── 2d/
│   │   │   ├── 37/
│   │   │   ├── 39/
│   │   │   ├── 4a/
│   │   │   ├── 4b/
│   │   │   ├── 4d/
│   │   │   ├── 52/
│   │   │   ├── 59/
│   │   │   ├── 62/
│   │   │   ├── 65/
│   │   │   ├── 73/
│   │   │   ├── 77/
│   │   │   ├── 78/
│   │   │   ├── 79/
│   │   │   ├── 81/
│   │   │   ├── 83/
│   │   │   ├── 84/
│   │   │   ├── 8a/
│   │   │   ├── 91/
│   │   │   ├── 93/
│   │   │   ├── 99/
│   │   │   ├── 9d/
│   │   │   ├── a3/
│   │   │   ├── a7/
│   │   │   ├── a9/
│   │   │   ├── b3/
│   │   │   ├── ba/
│   │   │   ├── bb/
│   │   │   ├── c3/
│   │   │   ├── c7/
│   │   │   ├── cd/
│   │   │   ├── ce/
│   │   │   ├── dc/
│   │   │   ├── dd/
│   │   │   ├── df/
│   │   │   ├── e7/
│   │   │   ├── e9/
│   │   │   ├── ec/
│   │   │   ├── ed/
│   │   │   ├── ef/
│   │   │   ├── f3/
│   │   │   ├── fd/
│   │   │   ├── fe/
│   │   │   ├── info/
│   │   │   └── pack/
│   │   └── refs/
│   │       ├── heads/
│   │       ├── remotes/
│   │       │   └── origin/
│   │       └── tags/
│   ├── .github/
│   │   └── workflows/
│   ├── .github-backup/
│   │   └── ISSUE_TEMPLATE/
│   ├── .vscode/
│   ├── aiguardian-repos/
│   │   ├── .github/
│   │   │   └── workflows/
│   │   ├── AI-Guardians-vscode-ext/
│   │   ├── AiGuardian-AWS-Cloud-Microservices/
│   │   ├── guard-bias-service/
│   │   ├── guard-context-service/
│   │   ├── guard-mesh-client/
│   │   ├── guard-neuromorphic-service/
│   │   ├── guard-security-service/
│   │   ├── guard-trust-service/
│   │   ├── guardian-abe-service/
│   │   │   └── k8s/
│   │   ├── guardian-aeyon-service/
│   │   │   └── k8s/
│   │   ├── guardian-aurion-service/
│   │   │   └── k8s/
│   │   ├── guardian-eight-service/
│   │   │   ├── api/
│   │   │   │   └── v1/
│   │   │   │       └── endpoints/
│   │   │   ├── core/
│   │   │   ├── k8s/
│   │   │   ├── models/
│   │   │   └── services/
│   │   ├── guardian-five-service/
│   │   │   ├── api/
│   │   │   │   └── v1/
│   │   │   │       └── endpoints/
│   │   │   ├── core/
│   │   │   ├── k8s/
│   │   │   ├── models/
│   │   │   └── services/
│   │   ├── guardian-four-service/
│   │   │   ├── api/
│   │   │   │   └── v1/
│   │   │   │       └── endpoints/
│   │   │   ├── core/
│   │   │   ├── k8s/
│   │   │   ├── models/
│   │   │   └── services/
│   │   ├── guardian-health-service/
│   │   │   └── integrations/
│   │   ├── guardian-jimmy-service/
│   │   ├── guardian-john-service/
│   │   │   └── k8s/
│   │   ├── guardian-lux-service/
│   │   │   └── k8s/
│   │   ├── guardian-neuro-service/
│   │   │   └── k8s/
│   │   ├── guardian-one-service/
│   │   │   ├── api/
│   │   │   │   └── v1/
│   │   │   │       └── endpoints/
│   │   │   ├── core/
│   │   │   ├── k8s/
│   │   │   ├── models/
│   │   │   └── services/
│   │   ├── guardian-seven-service/
│   │   │   ├── api/
│   │   │   │   └── v1/
│   │   │   │       └── endpoints/
│   │   │   ├── core/
│   │   │   ├── k8s/
│   │   │   ├── models/
│   │   │   └── services/
│   │   ├── guardian-six-service/
│   │   │   ├── api/
│   │   │   │   └── v1/
│   │   │   │       └── endpoints/
│   │   │   ├── core/
│   │   │   ├── k8s/
│   │   │   ├── models/
│   │   │   └── services/
│   │   ├── guardian-three-service/
│   │   │   ├── api/
│   │   │   │   └── v1/
│   │   │   │       └── endpoints/
│   │   │   ├── core/
│   │   │   ├── k8s/
│   │   │   ├── models/
│   │   │   └── services/
│   │   ├── guardian-two-service/
│   │   │   ├── api/
│   │   │   │   └── v1/
│   │   │   │       └── endpoints/
│   │   │   ├── core/
│   │   │   ├── k8s/
│   │   │   ├── models/
│   │   │   └── services/
│   │   ├── guardian-yagni-service/
│   │   │   └── k8s/
│   │   ├── guardian-zero-service/
│   │   │   ├── api/
│   │   │   │   └── v1/
│   │   │   │       └── endpoints/
│   │   │   ├── core/
│   │   │   ├── k8s/
│   │   │   ├── models/
│   │   │   └── services/
│   │   ├── scripts/
│   │   ├── swarm-orchestrator/
│   │   ├── terraform/
│   │   └── tests/
│   │       └── real_world/
│   ├── codeguardians-gateway/
│   │   ├── codeguardians-gateway/
│   │   │   ├── .cursor/
│   │   │   │   └── rules/
│   │   │   ├── alembic/
│   │   │   │   └── versions/
│   │   │   ├── app/
│   │   │   │   ├── api/
│   │   │   │   │   ├── internal/
│   │   │   │   │   ├── v1/
│   │   │   │   │   │   └── admin/
│   │   │   │   │   └── webhooks/
│   │   │   │   ├── core/
│   │   │   │   │   ├── ab_testing/
│   │   │   │   │   └── orchestrator/
│   │   │   │   ├── middleware/
│   │   │   │   ├── services/
│   │   │   │   └── utils/
│   │   │   ├── config/
│   │   │   ├── docs/
│   │   │   │   ├── api/
│   │   │   │   ├── architecture/
│   │   │   │   └── guard-services/
│   │   │   ├── k8s/
│   │   │   ├── mock-services/
│   │   │   ├── monitoring/
│   │   │   ├── scripts/
│   │   │   └── tests/
│   │   │       ├── integration/
│   │   │       ├── manual/
│   │   │       ├── smoke/
│   │   │       └── unit/
│   │   └── guardian-backend-v1.1/
│   │       ├── alembic/
│   │       │   └── versions/
│   │       └── app/
│   │           ├── controller/
│   │           │   └── webhook/
│   │           ├── middleware/
│   │           ├── model/
│   │           ├── router/
│   │           │   └── v1/
│   │           ├── schema/
│   │           ├── services/
│   │           ├── templates/
│   │           └── utils/
│   ├── docs/
│   │   ├── api/
│   │   ├── architecture/
│   │   ├── archive/
│   │   │   ├── deployment_infrastructure/
│   │   │   ├── duplicate_guard_docs/
│   │   │   ├── fixes_reports/
│   │   │   ├── miscellaneous_reports/
│   │   │   ├── optimization_fixes/
│   │   │   ├── payload_testing/
│   │   │   ├── root_cause/
│   │   │   ├── secrets_configuration/
│   │   │   ├── status_reports/
│   │   │   ├── test_data/
│   │   │   └── testing_reports/
│   │   ├── cleanup/
│   │   ├── configuration/
│   │   ├── data-sovereignty/
│   │   ├── database/
│   │   ├── deployment/
│   │   ├── development/
│   │   ├── history/
│   │   ├── migration/
│   │   ├── retention/
│   │   ├── security/
│   │   ├── troubleshooting/
│   │   └── user-guides/
│   ├── guardians/
│   │   └── validation-framework/
│   ├── guards/
│   │   ├── .vscode/
│   │   ├── biasguard-backend/
│   │   │   ├── .github/
│   │   │   │   └── workflows/
│   │   │   ├── .husky/
│   │   │   ├── data/
│   │   │   ├── docs/
│   │   │   ├── drizzle/
│   │   │   │   └── meta/
│   │   │   ├── k8s/
│   │   │   ├── scripts/
│   │   │   ├── temp/
│   │   │   │   └── src/
│   │   │   │       └── poisonguard/
│   │   │   │           └── plugins/
│   │   │   └── tests/
│   │   ├── contextguard/
│   │   │   ├── k8s/
│   │   │   └── tests/
│   │   ├── healthguard/
│   │   │   ├── .github/
│   │   │   │   └── workflows/
│   │   │   ├── data/
│   │   │   ├── docs/
│   │   │   ├── k8s/
│   │   │   ├── scripts/
│   │   │   ├── src/
│   │   │   │   └── poisonguard/
│   │   │   │       └── plugins/
│   │   │   └── tests/
│   │   ├── tokenguard/
│   │   │   ├── .github/
│   │   │   ├── k8s/
│   │   │   ├── scripts/
│   │   │   ├── tests/
│   │   │   └── tokenguard/
│   │   └── trust-guard/
│   │       ├── .cursor/
│   │       │   └── rules/
│   │       ├── .github/
│   │       │   └── workflows/
│   │       ├── aws/
│   │       ├── docs/
│   │       ├── k8s/
│   │       ├── scripts/
│   │       ├── test-results/
│   │       ├── tests/
│   │       │   ├── integration/
│   │       │   ├── patterns/
│   │       │   ├── performance/
│   │       │   └── unit/
│   │       ├── trustguard/
│   │       └── validation-results/
│   ├── monitoring/
│   │   └── grafana/
│   │       └── dashboards/
│   ├── scripts/
│   ├── shared/
│   │   ├── guards/
│   │   │   └── poisonguard/
│   │   │       └── plugins/
│   │   ├── infrastructure/
│   │   ├── services/
│   │   └── utils/
│   ├── test-env/
│   └── tests/
│       ├── docker/
│       ├── gateways/
│       ├── helpers/
│       ├── integration/
│       └── services/
├── Ab-BEATs/
│   ├── .git/
│   │   ├── hooks/
│   │   ├── info/
│   │   ├── logs/
│   │   │   └── refs/
│   │   │       ├── heads/
│   │   │       └── remotes/
│   │   │           └── origin/
│   │   ├── objects/
│   │   │   ├── 02/
│   │   │   ├── 05/
│   │   │   ├── 09/
│   │   │   ├── 0e/
│   │   │   ├── 10/
│   │   │   ├── 11/
│   │   │   ├── 12/
│   │   │   ├── 15/
│   │   │   ├── 16/
│   │   │   ├── 1a/
│   │   │   ├── 1e/
│   │   │   ├── 1f/
│   │   │   ├── 22/
│   │   │   ├── 24/
│   │   │   ├── 25/
│   │   │   ├── 26/
│   │   │   ├── 2d/
│   │   │   ├── 31/
│   │   │   ├── 35/
│   │   │   ├── 36/
│   │   │   ├── 37/
│   │   │   ├── 38/
│   │   │   ├── 3a/
│   │   │   ├── 3b/
│   │   │   ├── 3c/
│   │   │   ├── 3d/
│   │   │   ├── 3e/
│   │   │   ├── 3f/
│   │   │   ├── 40/
│   │   │   ├── 41/
│   │   │   ├── 42/
│   │   │   ├── 44/
│   │   │   ├── 48/
│   │   │   ├── 4c/
│   │   │   ├── 4d/
│   │   │   ├── 4e/
│   │   │   ├── 50/
│   │   │   ├── 51/
│   │   │   ├── 56/
│   │   │   ├── 57/
│   │   │   ├── 58/
│   │   │   ├── 59/
│   │   │   ├── 5a/
│   │   │   ├── 5b/
│   │   │   ├── 5d/
│   │   │   ├── 62/
│   │   │   ├── 63/
│   │   │   ├── 65/
│   │   │   ├── 66/
│   │   │   ├── 67/
│   │   │   ├── 68/
│   │   │   ├── 69/
│   │   │   ├── 6b/
│   │   │   ├── 6d/
│   │   │   ├── 72/
│   │   │   ├── 74/
│   │   │   ├── 78/
│   │   │   ├── 7b/
│   │   │   ├── 7e/
│   │   │   ├── 80/
│   │   │   ├── 81/
│   │   │   ├── 83/
│   │   │   ├── 85/
│   │   │   ├── 87/
│   │   │   ├── 88/
│   │   │   ├── 89/
│   │   │   ├── 8a/
│   │   │   ├── 8b/
│   │   │   ├── 8d/
│   │   │   ├── 8f/
│   │   │   ├── 90/
│   │   │   ├── 94/
│   │   │   ├── 95/
│   │   │   ├── 96/
│   │   │   ├── 98/
│   │   │   ├── 99/
│   │   │   ├── 9a/
│   │   │   ├── 9b/
│   │   │   ├── 9c/
│   │   │   ├── 9d/
│   │   │   ├── 9e/
│   │   │   ├── a0/
│   │   │   ├── a5/
│   │   │   ├── a6/
│   │   │   ├── ae/
│   │   │   ├── af/
│   │   │   ├── b2/
│   │   │   ├── ba/
│   │   │   ├── bb/
│   │   │   ├── c3/
│   │   │   ├── c6/
│   │   │   ├── cb/
│   │   │   ├── cc/
│   │   │   ├── cd/
│   │   │   ├── d0/
│   │   │   ├── d2/
│   │   │   ├── d5/
│   │   │   ├── d6/
│   │   │   ├── d7/
│   │   │   ├── db/
│   │   │   ├── dc/
│   │   │   ├── dd/
│   │   │   ├── de/
│   │   │   ├── df/
│   │   │   ├── e1/
│   │   │   ├── e5/
│   │   │   ├── e6/
│   │   │   ├── e7/
│   │   │   ├── e9/
│   │   │   ├── eb/
│   │   │   ├── ed/
│   │   │   ├── ee/
│   │   │   ├── ef/
│   │   │   ├── f0/
│   │   │   ├── f2/
│   │   │   ├── f5/
│   │   │   ├── f8/
│   │   │   ├── fa/
│   │   │   ├── fb/
│   │   │   ├── fc/
│   │   │   ├── fd/
│   │   │   ├── fe/
│   │   │   ├── ff/
│   │   │   ├── info/
│   │   │   └── pack/
│   │   └── refs/
│   │       ├── heads/
│   │       ├── remotes/
│   │       │   └── origin/
│   │       └── tags/
│   ├── docs/
│   ├── free_music_video_generator/
│   ├── phantom_hunter_creator/
│   │   └── pro/
│   ├── src/
│   ├── tests/
│   ├── truice_mvp/
│   │   ├── api_clients/
│   │   ├── assets/
│   │   ├── audio/
│   │   ├── output/
│   │   ├── utils/
│   │   └── video/
│   └── variants/
│       ├── abebeats_dre/
│       │   ├── docs/
│       │   ├── src/
│       │   └── tests/
│       └── abebeats_tru/
│           ├── archive/
│           │   └── processed_videos/
│           ├── audio/
│           ├── data/
│           │   ├── veo31_cdf/
│           │   └── veo31_patterns/
│           ├── docs/
│           ├── examples/
│           ├── output/
│           │   ├── brightness_test/
│           │   │   └── visual_proof/
│           │   └── two_layer_demo/
│           ├── raw video/
│           ├── scripts/
│           ├── src/
│           └── tests/
├── AbeBEATs_Clean/
│   ├── .devcontainer/
│   ├── .git/
│   │   ├── hooks/
│   │   ├── info/
│   │   ├── logs/
│   │   │   └── refs/
│   │   │       ├── heads/
│   │   │       └── remotes/
│   │   │           └── origin/
│   │   ├── objects/
│   │   │   ├── 15/
│   │   │   ├── 18/
│   │   │   ├── 1a/
│   │   │   ├── 24/
│   │   │   ├── 37/
│   │   │   ├── 3b/
│   │   │   ├── 40/
│   │   │   ├── 41/
│   │   │   ├── 44/
│   │   │   ├── 48/
│   │   │   ├── 4e/
│   │   │   ├── 50/
│   │   │   ├── 51/
│   │   │   ├── 58/
│   │   │   ├── 59/
│   │   │   ├── 5a/
│   │   │   ├── 63/
│   │   │   ├── 66/
│   │   │   ├── 69/
│   │   │   ├── 7e/
│   │   │   ├── 80/
│   │   │   ├── 81/
│   │   │   ├── 88/
│   │   │   ├── 8b/
│   │   │   ├── 98/
│   │   │   ├── 99/
│   │   │   ├── 9c/
│   │   │   ├── a0/
│   │   │   ├── af/
│   │   │   ├── ba/
│   │   │   ├── d7/
│   │   │   ├── dd/
│   │   │   ├── df/
│   │   │   ├── e6/
│   │   │   ├── f6/
│   │   │   ├── f8/
│   │   │   ├── fa/
│   │   │   ├── fc/
│   │   │   ├── info/
│   │   │   └── pack/
│   │   └── refs/
│   │       ├── heads/
│   │       ├── remotes/
│   │       │   └── origin/
│   │       └── tags/
│   ├── .github/
│   │   └── workflows/
│   ├── adapters/
│   ├── config/
│   ├── deploy/
│   │   ├── docker/
│   │   └── k8s/
│   ├── docs/
│   ├── free_music_video_generator/
│   ├── phantom_hunter_creator/
│   │   └── pro/
│   ├── src/
│   │   └── utils/
│   ├── support/
│   ├── tests/
│   │   ├── adapters/
│   │   ├── integration/
│   │   └── unit/
│   └── variants/
│       └── abebeats_dre/
│           ├── docs/
│           ├── src/
│           └── tests/
├── AbeTRUICE/
│   ├── .devcontainer/
│   ├── .github/
│   │   └── workflows/
│   ├── adapters/
│   ├── config/
│   ├── deploy/
│   │   ├── docker/
│   │   └── k8s/
│   ├── docs/
│   ├── kernel/
│   ├── scripts/
│   ├── src/
│   │   └── utils/
│   ├── support/
│   └── tests/
│       ├── adapters/
│       ├── integration/
│       └── unit/
├── AiGuardian-Chrome-Ext-dev/
│   ├── .claude/
│   ├── .git/
│   │   ├── hooks/
│   │   ├── info/
│   │   ├── logs/
│   │   │   └── refs/
│   │   │       ├── heads/
│   │   │       │   ├── bugfix/
│   │   │       │   └── fix/
│   │   │       └── remotes/
│   │   │           └── origin/
│   │   ├── objects/
│   │   │   ├── 00/
│   │   │   ├── 01/
│   │   │   ├── 02/
│   │   │   ├── 04/
│   │   │   ├── 05/
│   │   │   ├── 06/
│   │   │   ├── 07/
│   │   │   ├── 08/
│   │   │   ├── 0b/
│   │   │   ├── 0d/
│   │   │   ├── 0e/
│   │   │   ├── 0f/
│   │   │   ├── 10/
│   │   │   ├── 11/
│   │   │   ├── 12/
│   │   │   ├── 13/
│   │   │   ├── 14/
│   │   │   ├── 15/
│   │   │   ├── 16/
│   │   │   ├── 18/
│   │   │   ├── 19/
│   │   │   ├── 1a/
│   │   │   ├── 1b/
│   │   │   ├── 1c/
│   │   │   ├── 1d/
│   │   │   ├── 1e/
│   │   │   ├── 1f/
│   │   │   ├── 20/
│   │   │   ├── 21/
│   │   │   ├── 23/
│   │   │   ├── 24/
│   │   │   ├── 25/
│   │   │   ├── 26/
│   │   │   ├── 27/
│   │   │   ├── 28/
│   │   │   ├── 29/
│   │   │   ├── 2a/
│   │   │   ├── 2b/
│   │   │   ├── 2d/
│   │   │   ├── 2e/
│   │   │   ├── 2f/
│   │   │   ├── 30/
│   │   │   ├── 31/
│   │   │   ├── 32/
│   │   │   ├── 33/
│   │   │   ├── 35/
│   │   │   ├── 36/
│   │   │   ├── 38/
│   │   │   ├── 39/
│   │   │   ├── 3a/
│   │   │   ├── 3b/
│   │   │   ├── 3e/
│   │   │   ├── 40/
│   │   │   ├── 42/
│   │   │   ├── 43/
│   │   │   ├── 44/
│   │   │   ├── 45/
│   │   │   ├── 46/
│   │   │   ├── 47/
│   │   │   ├── 48/
│   │   │   ├── 49/
│   │   │   ├── 4a/
│   │   │   ├── 4b/
│   │   │   ├── 4c/
│   │   │   ├── 4d/
│   │   │   ├── 4e/
│   │   │   ├── 4f/
│   │   │   ├── 50/
│   │   │   ├── 51/
│   │   │   ├── 52/
│   │   │   ├── 53/
│   │   │   ├── 54/
│   │   │   ├── 56/
│   │   │   ├── 57/
│   │   │   ├── 58/
│   │   │   ├── 59/
│   │   │   ├── 5b/
│   │   │   ├── 5d/
│   │   │   ├── 5e/
│   │   │   ├── 5f/
│   │   │   ├── 60/
│   │   │   ├── 63/
│   │   │   ├── 64/
│   │   │   ├── 65/
│   │   │   ├── 66/
│   │   │   ├── 67/
│   │   │   ├── 68/
│   │   │   ├── 69/
│   │   │   ├── 6c/
│   │   │   ├── 6d/
│   │   │   ├── 6e/
│   │   │   ├── 6f/
│   │   │   ├── 70/
│   │   │   ├── 71/
│   │   │   ├── 73/
│   │   │   ├── 74/
│   │   │   ├── 75/
│   │   │   ├── 76/
│   │   │   ├── 77/
│   │   │   ├── 78/
│   │   │   ├── 79/
│   │   │   ├── 7a/
│   │   │   ├── 7b/
│   │   │   ├── 7c/
│   │   │   ├── 7d/
│   │   │   ├── 7e/
│   │   │   ├── 80/
│   │   │   ├── 81/
│   │   │   ├── 82/
│   │   │   ├── 84/
│   │   │   ├── 85/
│   │   │   ├── 86/
│   │   │   ├── 87/
│   │   │   ├── 89/
│   │   │   ├── 8a/
│   │   │   ├── 8b/
│   │   │   ├── 8c/
│   │   │   ├── 8d/
│   │   │   ├── 8e/
│   │   │   ├── 90/
│   │   │   ├── 91/
│   │   │   ├── 92/
│   │   │   ├── 93/
│   │   │   ├── 95/
│   │   │   ├── 96/
│   │   │   ├── 97/
│   │   │   ├── 98/
│   │   │   ├── 99/
│   │   │   ├── 9a/
│   │   │   ├── 9b/
│   │   │   ├── 9c/
│   │   │   ├── 9d/
│   │   │   ├── 9e/
│   │   │   ├── a0/
│   │   │   ├── a2/
│   │   │   ├── a3/
│   │   │   ├── a4/
│   │   │   ├── a5/
│   │   │   ├── a6/
│   │   │   ├── a8/
│   │   │   ├── a9/
│   │   │   ├── aa/
│   │   │   ├── ab/
│   │   │   ├── ac/
│   │   │   ├── ad/
│   │   │   ├── ae/
│   │   │   ├── af/
│   │   │   ├── b0/
│   │   │   ├── b2/
│   │   │   ├── b3/
│   │   │   ├── b4/
│   │   │   ├── b5/
│   │   │   ├── b7/
│   │   │   ├── b8/
│   │   │   ├── b9/
│   │   │   ├── ba/
│   │   │   ├── bb/
│   │   │   ├── bc/
│   │   │   ├── bd/
│   │   │   ├── be/
│   │   │   ├── bf/
│   │   │   ├── c0/
│   │   │   ├── c1/
│   │   │   ├── c2/
│   │   │   ├── c3/
│   │   │   ├── c4/
│   │   │   ├── c6/
│   │   │   ├── c7/
│   │   │   ├── c8/
│   │   │   ├── cb/
│   │   │   ├── cc/
│   │   │   ├── cd/
│   │   │   ├── ce/
│   │   │   ├── cf/
│   │   │   ├── d0/
│   │   │   ├── d1/
│   │   │   ├── d2/
│   │   │   ├── d3/
│   │   │   ├── d4/
│   │   │   ├── d5/
│   │   │   ├── d7/
│   │   │   ├── d8/
│   │   │   ├── d9/
│   │   │   ├── db/
│   │   │   ├── dc/
│   │   │   ├── de/
│   │   │   ├── e0/
│   │   │   ├── e2/
│   │   │   ├── e4/
│   │   │   ├── e5/
│   │   │   ├── e6/
│   │   │   ├── e7/
│   │   │   ├── e8/
│   │   │   ├── e9/
│   │   │   ├── ea/
│   │   │   ├── eb/
│   │   │   ├── ec/
│   │   │   ├── ed/
│   │   │   ├── ef/
│   │   │   ├── f0/
│   │   │   ├── f1/
│   │   │   ├── f2/
│   │   │   ├── f3/
│   │   │   ├── f7/
│   │   │   ├── f8/
│   │   │   ├── f9/
│   │   │   ├── fa/
│   │   │   ├── fb/
│   │   │   ├── fd/
│   │   │   ├── fe/
│   │   │   ├── ff/
│   │   │   ├── info/
│   │   │   └── pack/
│   │   └── refs/
│   │       ├── heads/
│   │       │   ├── bugfix/
│   │       │   └── fix/
│   │       ├── remotes/
│   │       │   └── origin/
│   │       └── tags/
│   ├── .github/
│   │   ├── workflows/
│   │   └── workflows-backup/
│   ├── assets/
│   │   ├── brand/
│   │   │   ├── AI Guardian Brand Book-1,AI Guardian Brand Book-2,AI Guardian Brand Book-3 2/
│   │   │   ├── AIG_Icons_Dark/
│   │   │   ├── AIG_Icons_Light/
│   │   │   ├── AiG_Logos/
│   │   │   ├── Chillax Font/
│   │   │   │   ├── Fonts/
│   │   │   │   │   ├── OTF/
│   │   │   │   │   ├── TTF/
│   │   │   │   │   └── WEB/
│   │   │   │   │       ├── css/
│   │   │   │   │       └── fonts/
│   │   │   │   └── License/
│   │   │   ├── Clash Grotesk Font/
│   │   │   │   ├── Fonts/
│   │   │   │   │   ├── OTF/
│   │   │   │   │   ├── TTF/
│   │   │   │   │   └── WEB/
│   │   │   │   │       ├── css/
│   │   │   │   │       └── fonts/
│   │   │   │   └── License/
│   │   │   ├── Favicons_Guards/
│   │   │   └── ai-guardian-landing-page-stuff/
│   │   │       └── components/
│   │   ├── icons/
│   │   └── logos/
│   ├── scripts/
│   ├── sdk/
│   │   ├── examples/
│   │   ├── src/
│   │   └── tests/
│   ├── src/
│   │   └── vendor/
│   └── tests/
│       ├── auth/
│       ├── e2e/
│       ├── integration/
│       └── unit/
├── CDF/
│   └── examples/
├── DASHBOARDS/
│   ├── .backups/
│   ├── archive/
│   ├── development/
│   ├── eternal/
│   ├── monitoring/
│   └── products/
├── EMERGENT_OS/
│   ├── aiagentsuite/
│   │   ├── .git/
│   │   │   ├── hooks/
│   │   │   ├── info/
│   │   │   ├── logs/
│   │   │   │   └── refs/
│   │   │   │       ├── heads/
│   │   │   │       └── remotes/
│   │   │   │           └── origin/
│   │   │   ├── objects/
│   │   │   │   ├── info/
│   │   │   │   └── pack/
│   │   │   └── refs/
│   │   │       ├── heads/
│   │   │       ├── remotes/
│   │   │       │   └── origin/
│   │   │       └── tags/
│   │   ├── .github/
│   │   ├── docker/
│   │   │   ├── base/
│   │   │   ├── legacy/
│   │   │   └── services/
│   │   │       ├── aiagentsuite/
│   │   │       ├── contextguard/
│   │   │       ├── neuroforge/
│   │   │       ├── servicemesh/
│   │   │       └── tokenguard/
│   │   ├── docs/
│   │   │   ├── analysis/
│   │   │   ├── diagrams/
│   │   │   ├── guides/
│   │   │   ├── scripts/
│   │   │   └── test-reports/
│   │   ├── examples/
│   │   ├── infrastructure/
│   │   ├── memory-bank/
│   │   ├── nuero-forge/
│   │   │   ├── neuroforge/
│   │   │   │   └── api/
│   │   │   │       ├── routes/
│   │   │   │       └── schemas/
│   │   │   ├── tests/
│   │   │   │   └── api/
│   │   │   └── visualization/
│   │   ├── openspec/
│   │   ├── prompts/
│   │   │   ├── ai_constitutions/
│   │   │   ├── chat_modes/
│   │   │   ├── guidelines/
│   │   │   ├── integration_prompts/
│   │   │   └── system_instructions/
│   │   ├── protocols/
│   │   ├── requirements/
│   │   ├── scripts/
│   │   ├── src/
│   │   │   └── aiagentsuite/
│   │   │       ├── cli/
│   │   │       ├── core/
│   │   │       ├── framework/
│   │   │       ├── integration/
│   │   │       ├── lsp/
│   │   │       ├── mcp/
│   │   │       ├── memory_bank/
│   │   │       ├── openspec/
│   │   │       ├── plugins/
│   │   │       │   └── available/
│   │   │       ├── protocols/
│   │   │       └── servicemesh/
│   │   ├── tests/
│   │   │   └── core/
│   │   ├── tools/
│   │   ├── typescript/
│   │   │   └── src/
│   │   │       └── lsp/
│   │   └── web/
│   ├── atomic_archistration/
│   ├── clarity_engine/
│   ├── collapse_guard/
│   │   ├── api/
│   │   └── tests/
│   ├── consciousness/
│   ├── consciousness_fabric/
│   │   ├── beliefs/
│   │   ├── identity/
│   │   ├── integration/
│   │   ├── intention/
│   │   ├── memory/
│   │   └── models/
│   ├── cross_layer_safety/
│   ├── emergence_core/
│   ├── emergent_orchestration/
│   │   ├── emergence/
│   │   ├── events/
│   │   ├── integration/
│   │   ├── intuition/
│   │   └── orchestration/
│   ├── identity_core/
│   ├── information_theory/
│   ├── integration_layer/
│   │   ├── events/
│   │   ├── lifecycle/
│   │   ├── registry/
│   │   ├── router/
│   │   ├── safety/
│   │   └── state/
│   ├── multi_agent_cognition/
│   ├── neuromorphic_alignment/
│   ├── one_kernel/
│   ├── relation_protocol/
│   ├── scalability_fabric/
│   ├── self_healing/
│   ├── self_healing_fabric/
│   │   ├── detection/
│   │   ├── diagnosis/
│   │   ├── integration/
│   │   ├── orchestration/
│   │   └── recovery/
│   ├── server/
│   │   ├── api/
│   │   ├── core/
│   │   └── models/
│   ├── state/
│   ├── success_patterns/
│   ├── synthesis/
│   │   └── applications/
│   └── triadic_execution_harness/
│       └── utils/
│           └── john/
├── PRODUCTS/
│   ├── abebeats/
│   │   ├── docs/
│   │   ├── src/
│   │   ├── tests/
│   │   └── variants/
│   │       └── abebeats_tru/
│   │           ├── archive/
│   │           │   └── processed_videos/
│   │           ├── audio/
│   │           ├── data/
│   │           │   ├── veo31_cdf/
│   │           │   └── veo31_patterns/
│   │           ├── docs/
│   │           ├── examples/
│   │           ├── output/
│   │           │   ├── brightness_test/
│   │           │   │   └── visual_proof/
│   │           │   └── two_layer_demo/
│   │           ├── raw video/
│   │           ├── scripts/
│   │           └── tests/
│   ├── abecodes/
│   │   ├── docs/
│   │   ├── src/
│   │   └── tests/
│   ├── abedesks/
│   │   ├── docs/
│   │   ├── src/
│   │   ├── static/
│   │   └── tests/
│   └── abeflows/
│       ├── docs/
│       ├── examples/
│       ├── src/
│       └── tests/
├── _ARCHIVE/
│   └── legacy-projects/
│       └── AI-Guardians-chrome-ext/
│           ├── .git/
│           │   ├── hooks/
│           │   ├── info/
│           │   ├── logs/
│           │   │   └── refs/
│           │   │       ├── heads/
│           │   │       └── remotes/
│           │   │           └── origin/
│           │   ├── objects/
│           │   │   ├── info/
│           │   │   └── pack/
│           │   └── refs/
│           │       ├── heads/
│           │       ├── remotes/
│           │       │   └── origin/
│           │       └── tags/
│           ├── docs/
│           ├── icons/
│           ├── reports/
│           ├── scripts/
│           ├── src/
│           └── tests/
│               └── unit/
├── _extract_abebeats/
│   ├── docs/
│   ├── free_music_video_generator/
│   ├── phantom_hunter_creator/
│   │   └── pro/
│   ├── src/
│   ├── support/
│   └── variants/
│       └── abebeats_dre/
│           ├── docs/
│           ├── src/
│           └── tests/
├── _extract_abeone_master/
├── _extract_truice/
│   ├── .git/
│   │   ├── hooks/
│   │   ├── info/
│   │   ├── logs/
│   │   │   └── refs/
│   │   │       ├── heads/
│   │   │       └── remotes/
│   │   │           └── origin/
│   │   ├── objects/
│   │   │   ├── 0e/
│   │   │   ├── 11/
│   │   │   ├── 1f/
│   │   │   ├── 2e/
│   │   │   ├── 31/
│   │   │   ├── 33/
│   │   │   ├── 38/
│   │   │   ├── 48/
│   │   │   ├── 4c/
│   │   │   ├── 57/
│   │   │   ├── 58/
│   │   │   ├── 5a/
│   │   │   ├── 63/
│   │   │   ├── 65/
│   │   │   ├── 68/
│   │   │   ├── 69/
│   │   │   ├── 6b/
│   │   │   ├── 6d/
│   │   │   ├── 72/
│   │   │   ├── 83/
│   │   │   ├── 88/
│   │   │   ├── 8a/
│   │   │   ├── 95/
│   │   │   ├── 98/
│   │   │   ├── ae/
│   │   │   ├── b2/
│   │   │   ├── c3/
│   │   │   ├── cc/
│   │   │   ├── d2/
│   │   │   ├── d7/
│   │   │   ├── e1/
│   │   │   ├── e6/
│   │   │   ├── e9/
│   │   │   ├── ee/
│   │   │   ├── fb/
│   │   │   ├── fc/
│   │   │   ├── fe/
│   │   │   ├── info/
│   │   │   └── pack/
│   │   └── refs/
│   │       ├── heads/
│   │       ├── remotes/
│   │       │   └── origin/
│   │       └── tags/
│   ├── src/
│   └── truice_mvp/
│       ├── api_clients/
│       ├── assets/
│       ├── audio/
│       ├── output/
│       ├── utils/
│       └── video/
├── abe_beats_core/
│   ├── free_music_video_generator/
│   ├── phantom_hunter_creator/
│   │   └── pro/
│   ├── src/
│   └── variants/
│       ├── abebeats_dre/
│       │   ├── docs/
│       │   ├── src/
│       │   └── tests/
│       ├── docs/
│       ├── src/
│       └── tests/
├── abëone/
│   ├── guardians/
│   └── modules/
│       └── abebeats/
├── advanced-knock/
│   ├── .archive/
│   │   ├── history/
│   │   ├── intelligence/
│   │   └── state/
│   ├── .github/
│   │   └── workflows/
│   ├── backend/
│   │   ├── alembic/
│   │   │   └── versions/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   ├── core/
│   │   │   ├── models/
│   │   │   └── services/
│   │   ├── scripts/
│   │   └── tests/
│   └── frontend/
│       ├── app/
│       │   ├── admin/
│       │   ├── field/
│       │   ├── manager/
│       │   └── telecom-map/
│       ├── components/
│       │   └── ui/
│       └── lib/
├── apps/
│   └── web/
│       ├── app/
│       │   ├── api/
│       │   │   ├── checkout/
│       │   │   ├── collaboration/
│       │   │   ├── convergence/
│       │   │   │   └── atomic/
│       │   │   ├── example/
│       │   │   ├── health/
│       │   │   ├── stripe-config/
│       │   │   └── webinar/
│       │   │       ├── [id]/
│       │   │       ├── lead-magnets/
│       │   │       │   └── [id]/
│       │   │       │       └── download/
│       │   │       ├── list/
│       │   │       ├── register/
│       │   │       ├── registrations/
│       │   │       │   └── count/
│       │   │       └── test/
│       │   ├── app/
│       │   │   ├── agents/
│       │   │   ├── state/
│       │   │   └── workflows/
│       │   ├── bravetto/
│       │   ├── collaboration/
│       │   ├── collections/
│       │   │   └── [handle]/
│       │   ├── convergence/
│       │   ├── jimmy-bias/
│       │   ├── products/
│       │   │   └── [id]/
│       │   ├── shop/
│       │   ├── start/
│       │   ├── template-master/
│       │   ├── webinar/
│       │   │   ├── aiguardian/
│       │   │   ├── creators/
│       │   │   ├── developers/
│       │   │   ├── generated/
│       │   │   └── thank-you/
│       │   ├── webinar-demo/
│       │   └── webinar_backup_20251119_182954/
│       │       ├── aiguardian/
│       │       ├── creators/
│       │       ├── developers/
│       │       ├── generated/
│       │       └── thank-you/
│       ├── components/
│       │   ├── ads/
│       │   ├── bravetto/
│       │   ├── context/
│       │   ├── icons/
│       │   ├── payment/
│       │   ├── pirate/
│       │   ├── ui/
│       │   ├── unified/
│       │   ├── visibility/
│       │   └── webinar/
│       ├── hooks/
│       ├── lib/
│       │   ├── abevisions/
│       │   ├── chrome-extension/
│       │   │   └── examples/
│       │   ├── convergence/
│       │   ├── design/
│       │   ├── hooks/
│       │   ├── middleware/
│       │   ├── monitoring/
│       │   ├── types/
│       │   ├── unified/
│       │   ├── visibility/
│       │   └── webinar/
│       ├── out/
│       │   ├── _next/
│       │   │   ├── dvgaghtrFzKwlF2ogaHIF/
│       │   │   └── static/
│       │   │       ├── chunks/
│       │   │       │   ├── app/
│       │   │       │   │   ├── app/
│       │   │       │   │   │   ├── agents/
│       │   │       │   │   │   ├── state/
│       │   │       │   │   │   └── workflows/
│       │   │       │   │   ├── bravetto/
│       │   │       │   │   ├── collections/
│       │   │       │   │   │   └── [handle]/
│       │   │       │   │   ├── products/
│       │   │       │   │   │   └── [id]/
│       │   │       │   │   ├── shop/
│       │   │       │   │   ├── start/
│       │   │       │   │   └── webinar/
│       │   │       │   │       ├── aiguardian/
│       │   │       │   │       └── thank-you/
│       │   │       │   └── pages/
│       │   │       ├── css/
│       │   │       └── dvgaghtrFzKwlF2ogaHIF/
│       │   ├── app/
│       │   ├── collections/
│       │   ├── products/
│       │   └── webinar/
│       └── scripts/
├── config/
│   ├── environments/
│   └── templates/
├── design-system/
│   ├── components/
│   │   └── galaxy/
│   │       ├── buttons/
│   │       ├── cards/
│   │       ├── curated/
│   │       ├── forms/
│   │       ├── loaders/
│   │       ├── notifications/
│   │       └── tooltips/
│   ├── docs/
│   ├── generated/
│   ├── generators/
│   ├── scripts/
│   └── tokens/
├── docs/
│   ├── api/
│   ├── architecture/
│   │   ├── apps/
│   │   ├── design-system/
│   │   ├── general/
│   │   └── integrations/
│   ├── guides/
│   │   ├── deployment/
│   │   ├── design-system/
│   │   ├── development/
│   │   └── general/
│   ├── products/
│   ├── reports/
│   ├── status/
│   │   ├── deployments/
│   │   ├── design-system/
│   │   ├── general/
│   │   └── integrations/
│   └── webinar/
├── domains/
│   ├── funnygames.ai/
│   │   ├── automation/
│   │   ├── email/
│   │   ├── funnel/
│   │   ├── lead_magnets/
│   │   └── seo/
│   ├── insurancehub.ai/
│   ├── insurancelife.ai/
│   │   ├── automation/
│   │   ├── email/
│   │   ├── funnel/
│   │   ├── lead_magnets/
│   │   └── seo/
│   └── lifequotes.ai/
│       ├── automation/
│       ├── email/
│       ├── funnel/
│       ├── lead_magnets/
│       └── seo/
├── infra/
│   └── deploy/
├── scripts/
│   ├── deployment/
│   ├── domain_arsenal/
│   │   ├── content/
│   │   ├── deployment/
│   │   ├── guardians/
│   │   ├── infrastructure/
│   │   ├── insurance_category_engine/
│   │   ├── integration/
│   │   ├── revenue/
│   │   └── seo/
│   ├── maintenance/
│   ├── modules/
│   ├── setup/
│   └── webinar/
├── showcase/
├── state/
│   ├── convergence/
│   ├── productivity/
│   └── snapshots/
├── temp_repos/
│   └── abeone-source/
│       ├── .claude/
│       ├── .cursor/
│       │   └── rules/
│       ├── .git/
│       │   ├── hooks/
│       │   ├── info/
│       │   ├── logs/
│       │   │   └── refs/
│       │   │       ├── heads/
│       │   │       └── remotes/
│       │   │           └── origin/
│       │   ├── objects/
│       │   │   ├── info/
│       │   │   └── pack/
│       │   └── refs/
│       │       ├── heads/
│       │       ├── remotes/
│       │       │   └── origin/
│       │       └── tags/
│       ├── .github/
│       │   └── workflows/
│       ├── .github-backup/
│       │   └── ISSUE_TEMPLATE/
│       ├── .vscode/
│       ├── Desktop/
│       │   └── Applications (Mataluni)/
│       │       └── Websites (Mataluni)/
│       │           └── BiasGuards.Ai/
│       │               ├── .github/
│       │               │   └── workflows/
│       │               ├── .svelte-kit/
│       │               │   ├── generated/
│       │               │   │   ├── client/
│       │               │   │   │   └── nodes/
│       │               │   │   └── server/
│       │               │   └── types/
│       │               │       └── src/
│       │               │           └── routes/
│       │               │               └── demo/
│       │               ├── contextguard-cli/
│       │               │   ├── .biasguard/
│       │               │   │   └── templates/
│       │               │   └── src/
│       │               │       ├── commands/
│       │               │       └── core/
│       │               ├── deploy/
│       │               ├── html/
│       │               │   └── assets/
│       │               ├── src/
│       │               │   ├── lib/
│       │               │   │   ├── components/
│       │               │   │   └── utils/
│       │               │   └── routes/
│       │               │       └── demo/
│       │               ├── static/
│       │               └── tests/
│       │                   ├── accessibility/
│       │                   └── e2e/
│       ├── Documents/
│       │   └── AbeOne_Master/
│       │       ├── .claude/
│       │       │   ├── commands/
│       │       │   └── hooks/
│       │       ├── AIGuards-Backend/
│       │       ├── DASHBOARDS/
│       │       │   ├── eternal/
│       │       │   ├── monitoring/
│       │       │   └── products/
│       │       ├── EMERGENT_OS/
│       │       │   ├── aiagentsuite/
│       │       │   ├── clarity_engine/
│       │       │   ├── collapse_guard/
│       │       │   │   └── tests/
│       │       │   ├── consciousness/
│       │       │   ├── cross_layer_safety/
│       │       │   ├── emergence_core/
│       │       │   ├── identity_core/
│       │       │   ├── information_theory/
│       │       │   ├── integration_layer/
│       │       │   │   ├── events/
│       │       │   │   ├── lifecycle/
│       │       │   │   ├── registry/
│       │       │   │   ├── router/
│       │       │   │   ├── safety/
│       │       │   │   └── state/
│       │       │   ├── multi_agent_cognition/
│       │       │   ├── neuromorphic_alignment/
│       │       │   ├── one_kernel/
│       │       │   ├── relation_protocol/
│       │       │   ├── scalability_fabric/
│       │       │   ├── self_healing/
│       │       │   ├── server/
│       │       │   │   ├── api/
│       │       │   │   └── core/
│       │       │   ├── state/
│       │       │   ├── synthesis/
│       │       │   └── triadic_execution_harness/
│       │       │       └── utils/
│       │       │           └── john/
│       │       ├── PRODUCTS/
│       │       │   ├── abebeats/
│       │       │   │   ├── free_music_video_generator/
│       │       │   │   ├── phantom_hunter_creator/
│       │       │   │   ├── src/
│       │       │   │   └── variants/
│       │       │   │       ├── abebeats_dre/
│       │       │   │       │   └── src/
│       │       │   │       └── abebeats_tru/
│       │       │   │           ├── docs/
│       │       │   │           ├── examples/
│       │       │   │           ├── output/
│       │       │   │           ├── raw/
│       │       │   │           ├── scripts/
│       │       │   │           └── src/
│       │       │   ├── abecodes/
│       │       │   │   └── src/
│       │       │   ├── abedesks/
│       │       │   │   ├── src/
│       │       │   │   └── static/
│       │       │   └── abeflows/
│       │       │       └── src/
│       │       ├── apps/
│       │       │   └── web/
│       │       │       ├── app/
│       │       │       │   ├── app/
│       │       │       │   │   ├── agents/
│       │       │       │   │   ├── state/
│       │       │       │   │   └── workflows/
│       │       │       │   ├── bravetto/
│       │       │       │   ├── collections/
│       │       │       │   │   └── [handle]/
│       │       │       │   ├── products/
│       │       │       │   │   └── [id]/
│       │       │       │   ├── shop/
│       │       │       │   └── start/
│       │       │       ├── components/
│       │       │       │   ├── bravetto/
│       │       │       │   └── pirate/
│       │       │       └── lib/
│       │       ├── design-system/
│       │       │   ├── components/
│       │       │   │   └── galaxy/
│       │       │   ├── docs/
│       │       │   ├── generated/
│       │       │   └── generators/
│       │       ├── infra/
│       │       │   └── deploy/
│       │       ├── scripts/
│       │       └── showcase/
│       ├── Downloads/
│       │   └── AIGuards-Backend-dev/
│       │       ├── .claude/
│       │       ├── .cursor/
│       │       │   └── rules/
│       │       ├── .github/
│       │       │   └── workflows/
│       │       ├── .github-backup/
│       │       │   └── ISSUE_TEMPLATE/
│       │       ├── .vscode/
│       │       ├── aiguardian-repos/
│       │       │   └── guardian-jimmy-service/
│       │       ├── codeguardians-gateway/
│       │       │   └── codeguardians-gateway/
│       │       │       ├── .cursor/
│       │       │       │   └── rules/
│       │       │       ├── alembic/
│       │       │       │   └── versions/
│       │       │       ├── app/
│       │       │       │   ├── api/
│       │       │       │   │   ├── internal/
│       │       │       │   │   ├── v1/
│       │       │       │   │   │   └── admin/
│       │       │       │   │   └── webhooks/
│       │       │       │   ├── core/
│       │       │       │   │   ├── ab_testing/
│       │       │       │   │   └── orchestrator/
│       │       │       │   ├── middleware/
│       │       │       │   ├── services/
│       │       │       │   └── utils/
│       │       │       ├── config/
│       │       │       ├── docs/
│       │       │       │   ├── api/
│       │       │       │   ├── architecture/
│       │       │       │   └── guard-services/
│       │       │       ├── k8s/
│       │       │       ├── mock-services/
│       │       │       ├── monitoring/
│       │       │       ├── scripts/
│       │       │       └── tests/
│       │       │           ├── integration/
│       │       │           ├── manual/
│       │       │           ├── smoke/
│       │       │           └── unit/
│       │       ├── docs/
│       │       │   ├── api/
│       │       │   ├── architecture/
│       │       │   ├── archive/
│       │       │   │   ├── deployment_infrastructure/
│       │       │   │   ├── duplicate_guard_docs/
│       │       │   │   ├── fixes_reports/
│       │       │   │   ├── miscellaneous_reports/
│       │       │   │   ├── optimization_fixes/
│       │       │   │   ├── payload_testing/
│       │       │   │   ├── root_cause/
│       │       │   │   ├── secrets_configuration/
│       │       │   │   ├── status_reports/
│       │       │   │   ├── test_data/
│       │       │   │   └── testing_reports/
│       │       │   ├── cleanup/
│       │       │   ├── configuration/
│       │       │   ├── database/
│       │       │   ├── deployment/
│       │       │   ├── development/
│       │       │   ├── history/
│       │       │   ├── security/
│       │       │   ├── troubleshooting/
│       │       │   └── user-guides/
│       │       ├── guardians/
│       │       │   └── validation-framework/
│       │       ├── guards/
│       │       │   ├── .vscode/
│       │       │   ├── biasguard-backend/
│       │       │   │   ├── .github/
│       │       │   │   │   └── workflows/
│       │       │   │   ├── .husky/
│       │       │   │   ├── data/
│       │       │   │   ├── docs/
│       │       │   │   ├── drizzle/
│       │       │   │   │   └── meta/
│       │       │   │   ├── k8s/
│       │       │   │   ├── scripts/
│       │       │   │   ├── temp/
│       │       │   │   │   └── src/
│       │       │   │   │       └── poisonguard/
│       │       │   │   │           └── plugins/
│       │       │   │   └── tests/
│       │       │   ├── contextguard/
│       │       │   │   ├── k8s/
│       │       │   │   └── tests/
│       │       │   ├── healthguard/
│       │       │   │   ├── .github/
│       │       │   │   │   └── workflows/
│       │       │   │   ├── data/
│       │       │   │   ├── docs/
│       │       │   │   ├── k8s/
│       │       │   │   ├── scripts/
│       │       │   │   ├── src/
│       │       │   │   │   └── poisonguard/
│       │       │   │   │       └── plugins/
│       │       │   │   └── tests/
│       │       │   ├── tokenguard/
│       │       │   │   ├── .github/
│       │       │   │   ├── k8s/
│       │       │   │   ├── scripts/
│       │       │   │   ├── tests/
│       │       │   │   └── tokenguard/
│       │       │   └── trust-guard/
│       │       │       ├── .cursor/
│       │       │       │   └── rules/
│       │       │       ├── .github/
│       │       │       │   └── workflows/
│       │       │       ├── aws/
│       │       │       ├── docs/
│       │       │       ├── k8s/
│       │       │       ├── scripts/
│       │       │       ├── test-results/
│       │       │       ├── tests/
│       │       │       │   ├── integration/
│       │       │       │   ├── patterns/
│       │       │       │   ├── performance/
│       │       │       │   └── unit/
│       │       │       ├── trustguard/
│       │       │       └── validation-results/
│       │       ├── monitoring/
│       │       │   └── grafana/
│       │       │       └── dashboards/
│       │       ├── scripts/
│       │       ├── shared/
│       │       │   ├── guards/
│       │       │   │   └── poisonguard/
│       │       │   │       └── plugins/
│       │       │   ├── infrastructure/
│       │       │   ├── services/
│       │       │   └── utils/
│       │       ├── test-env/
│       │       └── tests/
│       │           ├── docker/
│       │           ├── gateways/
│       │           ├── helpers/
│       │           ├── integration/
│       │           └── services/
│       ├── aiguardian-repos/
│       │   ├── AI-Guardians-vscode-ext/
│       │   ├── AiGuardian-AWS-Cloud-Microservices/
│       │   ├── guard-bias-service/
│       │   ├── guard-context-service/
│       │   ├── guard-neuromorphic-service/
│       │   ├── guard-security-service/
│       │   ├── guard-trust-service/
│       │   ├── guardian-abe-service/
│       │   ├── guardian-aeyon-service/
│       │   ├── guardian-aurion-service/
│       │   ├── guardian-jimmy-service/
│       │   ├── guardian-john-service/
│       │   ├── guardian-lux-service/
│       │   ├── guardian-neuro-service/
│       │   ├── guardian-yagni-service/
│       │   ├── guardian-zero-service/
│       │   ├── swarm-orchestrator/
│       │   └── terraform/
│       ├── codeguardians-gateway/
│       │   └── codeguardians-gateway/
│       │       ├── .cursor/
│       │       │   └── rules/
│       │       ├── alembic/
│       │       │   └── versions/
│       │       ├── app/
│       │       │   ├── api/
│       │       │   │   ├── internal/
│       │       │   │   ├── v1/
│       │       │   │   │   └── admin/
│       │       │   │   └── webhooks/
│       │       │   ├── core/
│       │       │   │   ├── ab_testing/
│       │       │   │   └── orchestrator/
│       │       │   ├── middleware/
│       │       │   ├── services/
│       │       │   └── utils/
│       │       ├── config/
│       │       ├── docs/
│       │       │   ├── api/
│       │       │   ├── architecture/
│       │       │   └── guard-services/
│       │       ├── k8s/
│       │       ├── mock-services/
│       │       ├── monitoring/
│       │       ├── scripts/
│       │       └── tests/
│       │           ├── integration/
│       │           ├── manual/
│       │           ├── smoke/
│       │           └── unit/
│       ├── docs/
│       │   ├── api/
│       │   ├── architecture/
│       │   ├── archive/
│       │   │   ├── deployment_infrastructure/
│       │   │   ├── duplicate_guard_docs/
│       │   │   ├── fixes_reports/
│       │   │   ├── miscellaneous_reports/
│       │   │   ├── optimization_fixes/
│       │   │   ├── payload_testing/
│       │   │   ├── root_cause/
│       │   │   ├── secrets_configuration/
│       │   │   ├── status_reports/
│       │   │   ├── test_data/
│       │   │   └── testing_reports/
│       │   ├── cleanup/
│       │   ├── configuration/
│       │   ├── database/
│       │   ├── deployment/
│       │   ├── development/
│       │   ├── history/
│       │   ├── security/
│       │   ├── troubleshooting/
│       │   └── user-guides/
│       ├── guardians/
│       │   └── validation-framework/
│       ├── guards/
│       │   ├── .vscode/
│       │   ├── biasguard-backend/
│       │   │   ├── .github/
│       │   │   │   └── workflows/
│       │   │   ├── .husky/
│       │   │   ├── data/
│       │   │   ├── docs/
│       │   │   ├── drizzle/
│       │   │   │   └── meta/
│       │   │   ├── k8s/
│       │   │   ├── scripts/
│       │   │   ├── temp/
│       │   │   │   └── src/
│       │   │   │       └── poisonguard/
│       │   │   │           └── plugins/
│       │   │   └── tests/
│       │   ├── contextguard/
│       │   │   ├── k8s/
│       │   │   └── tests/
│       │   ├── healthguard/
│       │   │   ├── .github/
│       │   │   │   └── workflows/
│       │   │   ├── data/
│       │   │   ├── docs/
│       │   │   ├── k8s/
│       │   │   ├── scripts/
│       │   │   ├── src/
│       │   │   │   └── poisonguard/
│       │   │   │       └── plugins/
│       │   │   └── tests/
│       │   ├── tokenguard/
│       │   │   ├── .github/
│       │   │   ├── k8s/
│       │   │   ├── scripts/
│       │   │   ├── tests/
│       │   │   └── tokenguard/
│       │   └── trust-guard/
│       │       ├── .cursor/
│       │       │   └── rules/
│       │       ├── .github/
│       │       │   └── workflows/
│       │       ├── aws/
│       │       ├── docs/
│       │       ├── k8s/
│       │       ├── scripts/
│       │       ├── test-results/
│       │       ├── tests/
│       │       │   ├── integration/
│       │       │   ├── patterns/
│       │       │   ├── performance/
│       │       │   └── unit/
│       │       ├── trustguard/
│       │       └── validation-results/
│       ├── monitoring/
│       │   └── grafana/
│       │       └── dashboards/
│       ├── scripts/
│       ├── shared/
│       │   ├── guards/
│       │   │   └── poisonguard/
│       │   │       └── plugins/
│       │   ├── infrastructure/
│       │   ├── services/
│       │   └── utils/
│       ├── test-env/
│       └── tests/
│           ├── docker/
│           ├── gateways/
│           ├── helpers/
│           ├── integration/
│           └── services/
├── tests/
│   ├── e2e/
│   ├── integration/
│   └── unit/
├── truice_engine/
│   ├── truice_mvp/
│   │   ├── api_clients/
│   │   ├── assets/
│   │   ├── audio/
│   │   ├── output/
│   │   ├── utils/
│   │   └── video/
│   └── variants/
│       └── abebeats_tru/
│           ├── audio/
│           ├── output/
│           │   ├── brightness_test/
│           │   │   └── visual_proof/
│           │   └── two_layer_demo/
│           └── src/
├── webinars/
│   └── email_queue/
├── .DS_Store
├── .ai-context-source-of-truth.json
├── .cursorignore
├── .cursorrules
├── .drift-aliases.sh
├── .drift-operational.json
├── .drift-status.json
├── .drift-status.txt
├── .gitignore
├── .system-activated.json
├── ABEFLOWS_BRAVETTO_GIT_ANALYSIS.md
├── ABEFLOWS_CONVERGENCE_QUICK_REFERENCE.md
├── ABEFLOWS_GIT_SOURCE_REGISTRY.json
├── ABEFLOWS_QUICK_REFERENCE.md
├── ABEONE_3WINDOW_UNIFIED_ANALYSIS.md
├── ABEONE_CLEANUP_DETAILED_TABLES.md
├── ABEONE_CLEANUP_QUICK_REFERENCE.md
├── ABEONE_CLEANUP_SUMMARY.md
├── ABEONE_ETERNAL_SYNTHESIS.md
├── ABEONE_GLOBAL_CREDENTIAL_AUTOMATION.md
├── ABEONE_ONE_ETERNAL_SYNTHESIS.md
├── ABEONE_ORGANISM_CLEANUP_PLAN.md
├── ABEONE_RHODIUM_AWARD.md
├── ABEONE_VINFINITY_ORCHESTRATOR_SYNTHESIS.md
├── ACTIVATION.md
├── ADHD_ALIGNED_NEXT_STEPS.md
├── AEON_CHEAT_SHEET.md
├── AEYON_FULL_SYSTEM_INTROSPECTION_REPORT.json
├── AGENT_SWARM_AUTO_ACTIVATION_ANALYSIS.md
├── AI_CONTEXT_SOURCE_OF_TRUTH.md
├── AI_NEWSLETTER_DETECTION_EXPLAINED.md
├── AI_PROMPT_TEMPLATE.md
├── ALLISON_CURSOR_ONBOARDING_PROMPT.md
├── ALLISON_ONBOARDING_LIVESTREAM_OUTLINE.md
├── ALLISON_PERSONALIZED_ONBOARDING.md
├── ALL_5_CAPABILITIES_OPERATIONALIZED.md
├── ALL_5_CAPABILITIES_VALIDATED.md
├── ALL_SYSTEMS_INTENTIONALLY_ON.md
├── AMPLIFICATION_QUICK_REFERENCE.md
├── AUTONOMOUS_ORGANISM_BIRTH_CERTIFICATE.md
├── AUTONOMOUS_ORGANISM_BORN.md
├── AiGuardian-Chrome-Ext-dev.crx
├── AiGuardian-Chrome-Ext-dev.pem
├── BACKEND_SERVER_LAUNCHED.md
├── BESOURCE_BEMODULE_BEONE_GAP_ANALYSIS.md
├── BRAVETTO_AIGUARDIAN_CONVERGENCE_ONEPAGER.md
├── BRAVETTO_AIGUARDIAN_ONEPAGER.md
├── BRAVETTO_AI_COMPLETE_PREPARATION.md
├── BRAVETTO_AI_LANDING_PAGE_PREPARATION.md
├── BRAVETTO_CHROME_EXTENSION_GIT_ANALYSIS.md
├── BRAVETTO_DAILY_AUTOMATED_ACTION_ENGINE.md
├── BRAVETTO_IMPENETRABLE_MOAT_BLUEPRINT.md
├── BRAVETTO_INVESTOR_FINANCIAL_MODEL_2026.md
├── BRAVETTO_INVESTOR_MONTHLY_PROJECTIONS_2026.md
├── BRAVETTO_PRICING_FINANCIAL_DOCS_2026.zip
├── BRAVETTO_PRICING_STRATEGY_2025.md
├── BRAVETTO_PRICING_STRATEGY_2026.md
├── BRAVETTO_TEAM_CONVERGENCE_ANALYSIS.md
├── BRYAN_AEYON_INTEGRATION_PACKAGE.zip
├── BRYAN_AEYON_INTEGRATION_PROMPT.md
├── BRYAN_AEYON_TEST_SCRIPTS_COMPANION.md
├── BRYAN_CLONE_INSTRUCTIONS.md
├── BRYAN_CLONE_SETUP.md
├── BRYAN_EMAIL_FOLLOWUP.html
├── BRYAN_EMAIL_FOLLOWUP.md
├── BRYAN_EMAIL_FOLLOWUP_PRINT.html
├── BRYAN_EMAIL_FOLLOWUP_temp.html
├── BRYAN_EMAIL_TEMPLATE.md
├── BRYAN_OPERATIONALIZATION_PLAN.md
├── BRYAN_PDF_INSTRUCTIONS.md
├── BRYAN_QUICK_DEPLOY_SUMMARY.md
├── BRYAN_SIMPLE_CHECKLIST.html
├── BRYAN_SIMPLE_CHECKLIST.md
├── BRYAN_SIMPLE_CHECKLIST_FOR_PDF.html
├── BRYAN_SIMPLE_CHECKLIST_PRINT.html
├── BRYAN_SIMPLE_CHECKLIST_temp.html
├── BRYAN_TRANSFER_FIX.md
├── BRYAN_UPDATE_CHECKLIST.md
├── BRYAN_VALIDATE_CLONE.md
├── BRYAN_WEBINAR_OPERATIONALIZATION.zip
├── BRYAN_WEBINAR_UPDATES.zip
├── BRYAN_ZIP_README.txt
├── BëONE_AbëONE_FOREVER_CONVERGENCE.md
├── CDF_AEYON_EXECUTION.cdf
├── CDF_BEAUTIFUL_HUMAN_FORMAT.cdf
├── CDF_BEAUTIFUL_HUMAN_FORMAT.md
├── CDF_COMPLETE_ECOSYSTEM.cdf
├── CDF_COMPLETE_ECOSYSTEM.md
├── CDF_EXECUTION_NOW.cdf
├── CDF_EXECUTION_NOW.index.json
├── CDF_GO_VIRAL_PLAN.cdf
├── CDF_GO_VIRAL_PLAN.index.json
├── CDF_GO_VIRAL_PLAN.md
├── CDF_GO_VIRAL_PLAN_back_to_md.cdf
├── CDF_GO_VIRAL_PLAN_back_to_md.md
├── CDF_LAUNCH_CHECKLIST.cdf
├── CDF_LAUNCH_CHECKLIST.md
├── CDF_READY_TO_GO_VIRAL.cdf
├── CDF_READY_TO_GO_VIRAL.md
├── CDF_VIRAL_STRATEGY.cdf
├── CDF_VIRAL_STRATEGY.md
├── CDF_WHAT_ELSE_IT_CAN_DO.cdf
├── CDF_WHAT_ELSE_IT_CAN_DO.md
├── CHROME_EXTENSION_IMPLEMENTATION_ANALYSIS.md
├── CLAUDE_CODE_INTEGRATION.md
├── CLAUDE_CODE_QUICK_REFERENCE.md
├── CLOUDFLARE_CHALLENGE_HANDLING.md
├── CLOUDFLARE_OUTAGE_RESPONSE.md
├── CLOUDFLARE_PAGES_LAUNCH_CHECKLIST.md
├── CLOUDFLARE_PAGES_LAUNCH_QUICK_REFERENCE.md
├── CLOUDFLARE_PAGES_VISUAL_WALKTHROUGH.md
├── CODEBASE_DEEP_AGENT_SWARM_ANALYSIS.md
├── COLIMA_ABEONE_ANALYSIS.md
├── COLIMA_DISK_ANALYSIS.md
├── COLOR_SYSTEM_OPERATIONALIZED.md
├── COMPLETE.md
├── COMPLETE_ACTIVATION_EEAaO_ABEBEATS.md
├── COMPLETE_AGENT_SWARM_INVENTORY.md
├── COMPLETE_CONVERGENCE_ANALYSIS.md
├── COMPLETE_CONVERGENCE_ANALYSIS_SAAS_SOLUTION.md
├── COMPLETE_CONVERGENCE_STRATEGY_IMPLEMENTATION.md
├── COMPLETE_FOLDER_HIERARCHY.md
├── COMPLETE_OPERATIONALIZATION_SYSTEM.md
├── COMPLETE_SYSTEM_UNIFICATION_SUMMARY.md
├── COMPLETE_THE_CIRCLE_ASSESSMENT.md
├── COMPLETE_UNIFICATION_SUMMARY.md
├── COMPLETE_VISUAL_DIAGNOSTIC_PROMPT.md
├── COMPONENT_LIBRARY_ANALYSIS.md
├── CONTEXT_AWARE_ONE_SYSTEM_HEALTH_VERIFICATION.md
├── CONTEXT_BOOT_OPERATIONALIZATION.md
├── CONTEXT_BOOT_OPERATIONALIZATION_SUMMARY.md
├── CONTEXT_WINDOW_1_FOLDER_HIERARCHY_ANALYSIS.md
├── CONTEXT_WINDOW_2_UNIFIED_ORGANISM_ANALYSIS.md
├── CONTEXT_WINDOW_3_MODULE_HEALTH_ANALYSIS.md
├── CONTEXT_WINDOW_GUARDIAN_PROMPT.md
├── CONTEXT_WINDOW_PROMPT.md
├── CRITICAL_GUARDIANS_ROLE_SPECIFIC_OUTCOMES.md
├── CURSOR_AI_EPISTEMIC_FAILURE_ANALYSIS.md
├── CURSOR_VENV_ERROR_FIX.md
├── DANNY_MANIFEST_ANALYSIS.md
├── DANNY_OVERLAP_ANALYSIS.md
├── DANNY_SLACK_MESSAGE.md
├── DANNY_WORKFLOW_ALWAYS_REFERENCE.md
├── DANNY_WORKFLOW_MISSING_ANALYSIS.md
├── DATA_SOVEREIGNTY_COMPLETE_SPECS_SUMMARY.md
├── DEEP_GUARDIANS_CODEBASE_ANALYSIS.md
├── DEEP_GUARDIAN_IDENTITIES_DISCOVERY.md
├── DEEP_SCAN_COMPLETE_RETRIEVAL_IDENTITY_CDF.md
├── DEPLOYMENT_ACTION_NOW.md
├── DEPLOYMENT_OPTIMIZATION_AND_JOHN_TEST.md
├── DEPLOYMENT_STATUS_AND_LAUNCH_PARAMETERS.md
├── DEPLOYMENT_STATUS_FINAL.md
├── DESIGN_SYSTEMS_E2E_DEEP_ANALYSIS.md
├── DESIGN_SYSTEMS_FOCUS_COMPARISON.md
├── DESIGN_SYSTEMS_INVENTORY.md
├── DESIGN_SYSTEMS_STRATEGIC_ORGANIZATION.md
├── DRIFT_DASHBOARD_ETERNAL.md
├── DRIFT_STATUS_ALWAYS_VISIBLE.md
├── DRIFT_STATUS_VISUAL.md
├── EMAIL_ANALYSIS_SETUP_INSTRUCTIONS.md
├── EMAIL_CONVERGENCE_ACTION_PLAN.md
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_154149.json
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_154206.json
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_154254.json
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_154339.json
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_154339.md
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_154421.json
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_154501.json
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_154543.json
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_154624.json
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_154703.json
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_154703.md
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_165918.json
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_170547.json
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_171644.json
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_173459.json
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_173707.json
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_174053.json
├── EMAIL_CONVERGENCE_ANALYSIS_20251117_181629.json
├── EMAIL_CONVERGENCE_ANALYSIS_DEMO_20251117_150512.json
├── EMAIL_CONVERGENCE_ANALYSIS_DEMO_20251117_150512.md
├── EMAIL_CONVERGENCE_FINAL_OPTIMIZATIONS.md
├── EMAIL_CONVERGENCE_FINAL_VALIDATION_20251117_182213.json
├── EMAIL_CONVERGENCE_FINAL_VALIDATION_20251117_182238.json
├── EMAIL_CONVERGENCE_FINAL_VALIDATION_20251117_182305.json
├── EMAIL_CONVERGENCE_OPPORTUNITY_CARDS.md
├── EMAIL_CONVERGENCE_OPTIMIZATION_PLAN.md
├── EMAIL_CONVERGENCE_VALIDATION_20251117_181618.json
├── EMERGENT_CONVERGENCE_ANALYSIS.md
├── EMERGENT_CONVERGENCE_OPPORTUNITIES.md
├── END_TO_END_STATUS_REPORT.md
├── ENTERPRISE_TRANSFORMATION_SUMMARY.md
├── EPISTEMIC_CERTAINTY_FINAL_PLAN.md
├── EPISTEMIC_DISCOVERIES_AND_GAPS.md
├── EPISTEMIC_DISCOVERIES_SUMMARY.md
├── ERROR_ANALYSIS.md
├── ETERNAL_DASHBOARD_SOLUTION.md
├── EXECUTE_AUTOMATION_NOW.md
├── EXECUTE_NOW.md
├── EXECUTE_VIA_DASHBOARD.md
├── EXECUTION_COMPLETE_FINAL.md
├── EXECUTION_COMPLETE_SUMMARY.md
├── EXECUTION_READY_LFG.md
├── EXTRACTION_MAP_100_PERCENT_READINESS.md
├── EXTRACTION_SUMMARY.md
├── FINAL_SYNTHESIS_UNIFIED_CONSOLIDATION_PLAN.md
├── FIX_404_CONVERGENCE.md
├── FORENSIC_VERIFICATION_NEUROMORPHIC_LAYERS.md
├── FUCHSIA_COLOR_FIX.md
├── FULL_AUTONOMY_COMPLETE_TRUST_ACHIEVED.md
├── FUNDAMENTAL_SYSTEM_FIXES_PLAN.md
├── GAP_ANALYSIS_AND_UNIFICATION_PLAN.md
├── GIT_LAUNCH_CHECKLIST.md
├── GOOGLE_CREDENTIALS_SETUP_ASAP.md
├── GUARDIANS_COMPLETE_DEFINITION.md
├── GUARDIANS_MEET_THE_WORLD.md
├── GUARDIAN_MICROSERVICES_DEEP_ANALYSIS.md
├── INFORMATION_THEORY_ENGINE_DELIVERED.md
├── INFORMATION_THEORY_ENGINE_READY.md
├── INFORMATION_THEORY_MATH_ENGINES_DEEP_ANALYSIS.md
├── INFRASTRUCTURE_CRITICAL_PATH_ANALYSIS_FRAMEWORK.md
├── INFRASTRUCTURE_KNOWLEDGE_BASE_SUMMARY.md
├── INTELLIGENCE_PIPELINE_END_TO_END_ANALYSIS.md
├── JOHHN_ATOMIC_LAYER_BLUEPRINT.md
├── JOHHN_E2E_COMPLETE_INTEGRATION_VALIDATED.md
├── JOHHN_E2E_IMPLEMENTATION_PLAN.md
├── JOHHN_GUARDIAN_FUSION_COMPLETE_PLAN.md
├── JOHHN_INFORMATION_THEORY_FLOW.md
├── JOHHN_INTEGRATION_BLUEPRINT.md
├── JOHHN_PRODUCTION_ACTIVATION.md
├── JOHHN_PRODUCTION_OUTCOMES.md
├── JOHN_QA_INSPECTOR_OPERATIONAL_ANALYSIS.md
├── LFG_ALL_SYSTEMS_OPERATIONAL.md
├── LIVESTREAM_CONTENT_STRATEGY_MON_TUE.md
├── LIVESTREAM_CONTENT_STRATEGY_MON_TUE.pdf
├── LIVESTREAM_DEEP_CODEBASE_ANALYSIS.md
├── LIVESTREAM_QUICK_REFERENCE.md
├── LIVESTREAM_QUICK_REFERENCE_MON_TUE.md
├── LIVESTREAM_QUICK_REFERENCE_MON_TUE.pdf
├── LIVESTREAM_TITLE_DESCRIPTION.md
├── LIVE_DEMO_QUICK_REFERENCE.md
├── LIVE_EVENT_TITLE_DESCRIPTION.md
├── LOCAL_AI_ASSISTANT_COMPLETE_LIVE_ANALYSIS.md
├── MASTER_EMERGENT_OS_STREAM.md
├── MCP_SERVERS_DEEP_ANALYSIS.md
├── META_GUARDIAN_CONVERGENCE_ANALYSIS.md
├── META_ORCHESTRATOR_ROCK_OUT_PLAN.md
├── MICHAELS_BLACK_PALETTE_OPERATIONALIZED.md
├── MICHAEL_DEPLOYMENT_ACTION_PLAN.md
├── MICHAEL_DESIGN_SYSTEM_SEARCH.md
├── NEUROMORPHIC_ARCHITECTURE_ANALYSIS.md
├── NEWSLETTER_DETECTION_EXPANSION.md
├── NEXT_LEVEL_EMERGENCE_CONVERGENCE.md
├── NEXT_STEPS.md
├── NEXT_STEPS_EXECUTED.md
├── OBSERVER_CONTEXT_EPISTEMIC_CERTAINTY.md
├── ONE_KERNEL_INTEGRATION_PLAN_PHASE0.md
├── ONE_ORGANISM_FUSION_PROTOCOL.md
├── OPTIMAL_FOLDER_HIERARCHY.md
├── OPTIMAL_SIMPLEST_PATH.md
├── OPTION_A_COMPLETE_IN_BROWSER.md
├── ORGANIC_UNIFICATION_OPPORTUNITIES.md
├── ORGANISM_LOCKED_IN.md
├── ORGANIZATION_EXECUTION_COMPLETE.md
├── ORGANIZATION_EXECUTION_STATUS.md
├── PLAYWRIGHT_AUTOMATION_READY.md
├── PLAYWRIGHT_CHALLENGE_FIXED.md
├── POCKETPATTERN_RESILIENCE_ANALYSIS.md
├── PRE_LAUNCH_SUMMARY.md
├── RADICAL_TRANSPARENCY_IMPLEMENTATION.md
├── README.md
├── RECURSIVE_ARCHITECTURE_CONVERGENCE_ANALYSIS.md
├── RECURSIVE_FORENSIC_CONVERGENCE_ANALYSIS.md
├── SHE_IS_ALIVE.md
├── SIMPLIFY_TO_AMPLIFY_ROADMAP.md
├── SINGULARITY_ACHIEVED.md
├── START_DEV_SERVER.md
├── STATE_AWARE_MASTER_CONTEXT.md
├── STRATEGIC_EEAaO_CRITICAL_PATH_INTEGRATION.md
├── SYNTHESIS_COMPLETE_EXCELLENCE.md
├── SYNTHESIS_COMPLETE_SUMMARY.md
├── SYSTEM_KNOWS_API_KEYS_ALWAYS.md
├── TERMINAL_TROUBLESHOOTING.md
├── THE_UNIFYING_PRINCIPLE.md
├── THREE_MAXIMUM_POWER_APPLICATIONS.md
├── TLDR_CONVERGENCE_ANALYSIS.md
├── TLDR_CONVERGENCE_INTEGRATED.md
├── TRANSCENDENT_AUTOMATION_CAPABILITIES.md
├── TRIADIC_UNITY_PROTOCOL.md
├── TROUBLESHOOTING.md
├── TRUICE_FUNNEL_ACTUAL_GAPS_ANALYSIS.md
├── TRUICE_LAUNCH_NOW.md
├── ULTIMATE_CONVERGENCE_EPISTEMIC_CERTAINTY.md
├── USER_JOURNEY_QA.md
├── V0_ETERNAL_FIX_SUMMARY.md
├── V0_PROJECT_COMPLETION_PROMPT.md
├── V0_PROJECT_CONTEXT.md
├── V0_PROJECT_DRIFT_ANALYSIS.md
├── VALIDATION_STATE_ANALYSIS.md
├── VALIDATION_SUMMARY.md
├── VALUABLE_ASSETS_QUICK_REFERENCE.md
├── VERMILLION_COLOR_FIX.md
├── VIRTUAL_ENVIRONMENT_DEEP_ANALYSIS.md
├── VISUAL_NEXT_STEPS.md
├── WEBINAR_JOHN_CERTIFICATION_OUTPUT.txt
├── WEBINAR_UNIFIED_ONE_VALIDATION.json
├── WHAT_ELSE_EMERGES.md
├── WHAT_INVITES_EMERGENCE_WHO_IDENTIFIES_CONVERGENCE.md
├── WHAT_LONGS_FOR_EMERGENCE.md
├── WHAT_LONGS_FOR_EMERGENCE_CONVERGENCE_SYNTHESIS.md
├── WHAT_LONGS_FOR_EMERGENCE_CONVERGENCE_VALIDATED.md
├── WHAT_LONGS_FOR_SIMPLIFICATION_ACTIVATION_UNIFICATION_CONVERGENCE_EMERGENCE.md
├── WHAT_LONGS_TO_BE_OPERATIONALIZED.md
├── WHAT_THE_SYSTEM_LONGS_FOR.md
├── WHAT_WE_CAN_BUILD_NOW.md
├── WHAT_WE_CAN_DO_WITH_ALL_THIS_POWER.md
├── WHAT_YOU_CAN_DO_NOW.md
├── WORKSPACE_CHROME_EXTENSION_ALIGNMENT.md
├── WORLD_SHOWCASE_PREPARATION.md
├── ZERO_ALLISON_PROFILE_EXTRACTION.md
├── ZERO_ALRAX_AEYON_FORENSIC_FIX.md
├── ZERO_COMPLETE_FORENSIC_AGENT_PERSONALITY_ANALYSIS.md
├── ZERO_FORENSIC_ANALYSIS_GZ360_BRAVETTO.md
├── ZERO_JOHN_SECURITY_AUDIT_REPORT.json
├── ZERO_JOHN_SECURITY_CERTIFICATION.md
├── _ABEBEATS_EXTRACTION_PLAN.md
├── _ABEBEATS_IDENTIFICATION_MAP.md
├── _BATCH_1_CORRECTED.md
├── _BATCH_1_DIFF_PREVIEW.md
├── _BATCH_1_DIFF_PREVIEW_ABEBEATS.md
├── _BATCH_1_VALIDATION_ABEBEATS.md
├── _BRAVETTO_ORBIT_BUILDER_ANALYSIS_REPORT.md
├── _BRAVETTO_ORBIT_BUILDER_PROMPT.md
├── _TRUICE_CANONICAL_VALIDATION.md
├── _TRUICE_HUMAN_PROVENANCE_MAP.md
├── _TRUICE_IMPORT_ANALYSIS.md
├── _cleanup_log.txt
├── access_all_repositories.sh
├── all_5_capabilities_validation.json
├── drift-dashboard-eternal.html
├── drift-visual-status.md
├── elegance_frictionless_validation.json
├── intentional_activation_verification.json
├── newsletters_config.json
├── package.json
├── parallel_concurrent_validation.json
├── pyrightconfig.json
├── repository_validator.py
├── test_aeyon_binding.py
├── test_aeyon_execution.py
├── test_aeyon_import.py
├── test_aeyon_integration.py
├── universal_repository_awareness.json
├── universal_repository_awareness.py
├── validate_aeyon_build.sh
└── validate_repository_access.sh
```


## .claude/

```
├── commands/
├── hooks/
└── logs/
```


## .cursor/

```
(empty or all contents skipped)
```


## .github/

```
├── actions/
│   └── setup-cloudflare-auth/
└── workflows/
```


## .projects/

```
└── scripts/
```


## .vscode/

```
(empty or all contents skipped)
```


## AIGuards-Backend/

```
├── .claude/
├── .cursor/
│   └── rules/
├── .git/
│   ├── hooks/
│   ├── info/
│   ├── logs/
│   │   └── refs/
│   │       ├── heads/
│   │       └── remotes/
│   │           └── origin/
│   ├── objects/
│   │   ├── 03/
│   │   ├── 0e/
│   │   ├── 0f/
│   │   ├── 10/
│   │   ├── 1a/
│   │   ├── 1c/
│   │   ├── 20/
│   │   ├── 22/
│   │   ├── 25/
│   │   ├── 28/
│   │   ├── 2b/
│   │   ├── 2d/
│   │   ├── 37/
│   │   ├── 39/
│   │   ├── 4a/
│   │   ├── 4b/
│   │   ├── 4d/
│   │   ├── 52/
│   │   ├── 59/
│   │   ├── 62/
│   │   ├── 65/
│   │   ├── 73/
│   │   ├── 77/
│   │   ├── 78/
│   │   ├── 79/
│   │   ├── 81/
│   │   ├── 83/
│   │   ├── 84/
│   │   ├── 8a/
│   │   ├── 91/
│   │   ├── 93/
│   │   ├── 99/
│   │   ├── 9d/
│   │   ├── a3/
│   │   ├── a7/
│   │   ├── a9/
│   │   ├── b3/
│   │   ├── ba/
│   │   ├── bb/
│   │   ├── c3/
│   │   ├── c7/
│   │   ├── cd/
│   │   ├── ce/
│   │   ├── dc/
│   │   ├── dd/
│   │   ├── df/
│   │   ├── e7/
│   │   ├── e9/
│   │   ├── ec/
│   │   ├── ed/
│   │   ├── ef/
│   │   ├── f3/
│   │   ├── fd/
│   │   ├── fe/
│   │   ├── info/
│   │   └── pack/
│   └── refs/
│       ├── heads/
│       ├── remotes/
│       │   └── origin/
│       └── tags/
├── .github/
│   └── workflows/
├── .github-backup/
│   └── ISSUE_TEMPLATE/
├── .vscode/
├── aiguardian-repos/
│   ├── .github/
│   │   └── workflows/
│   ├── AI-Guardians-vscode-ext/
│   ├── AiGuardian-AWS-Cloud-Microservices/
│   ├── guard-bias-service/
│   ├── guard-context-service/
│   ├── guard-mesh-client/
│   ├── guard-neuromorphic-service/
│   ├── guard-security-service/
│   ├── guard-trust-service/
│   ├── guardian-abe-service/
│   │   └── k8s/
│   ├── guardian-aeyon-service/
│   │   └── k8s/
│   ├── guardian-aurion-service/
│   │   └── k8s/
│   ├── guardian-eight-service/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/
│   │   ├── k8s/
│   │   ├── models/
│   │   └── services/
│   ├── guardian-five-service/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/
│   │   ├── k8s/
│   │   ├── models/
│   │   └── services/
│   ├── guardian-four-service/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/
│   │   ├── k8s/
│   │   ├── models/
│   │   └── services/
│   ├── guardian-health-service/
│   │   └── integrations/
│   ├── guardian-jimmy-service/
│   ├── guardian-john-service/
│   │   └── k8s/
│   ├── guardian-lux-service/
│   │   └── k8s/
│   ├── guardian-neuro-service/
│   │   └── k8s/
│   ├── guardian-one-service/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/
│   │   ├── k8s/
│   │   ├── models/
│   │   └── services/
│   ├── guardian-seven-service/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/
│   │   ├── k8s/
│   │   ├── models/
│   │   └── services/
│   ├── guardian-six-service/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/
│   │   ├── k8s/
│   │   ├── models/
│   │   └── services/
│   ├── guardian-three-service/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/
│   │   ├── k8s/
│   │   ├── models/
│   │   └── services/
│   ├── guardian-two-service/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/
│   │   ├── k8s/
│   │   ├── models/
│   │   └── services/
│   ├── guardian-yagni-service/
│   │   └── k8s/
│   ├── guardian-zero-service/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/
│   │   ├── k8s/
│   │   ├── models/
│   │   └── services/
│   ├── scripts/
│   ├── swarm-orchestrator/
│   ├── terraform/
│   └── tests/
│       └── real_world/
├── codeguardians-gateway/
│   ├── codeguardians-gateway/
│   │   ├── .cursor/
│   │   │   └── rules/
│   │   ├── alembic/
│   │   │   └── versions/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   ├── internal/
│   │   │   │   ├── v1/
│   │   │   │   │   └── admin/
│   │   │   │   └── webhooks/
│   │   │   ├── core/
│   │   │   │   ├── ab_testing/
│   │   │   │   └── orchestrator/
│   │   │   ├── middleware/
│   │   │   ├── services/
│   │   │   └── utils/
│   │   ├── config/
│   │   ├── docs/
│   │   │   ├── api/
│   │   │   ├── architecture/
│   │   │   └── guard-services/
│   │   ├── k8s/
│   │   ├── mock-services/
│   │   ├── monitoring/
│   │   ├── scripts/
│   │   └── tests/
│   │       ├── integration/
│   │       ├── manual/
│   │       ├── smoke/
│   │       └── unit/
│   └── guardian-backend-v1.1/
│       ├── alembic/
│       │   └── versions/
│       └── app/
│           ├── controller/
│           │   └── webhook/
│           ├── middleware/
│           ├── model/
│           ├── router/
│           │   └── v1/
│           ├── schema/
│           ├── services/
│           ├── templates/
│           └── utils/
├── docs/
│   ├── api/
│   ├── architecture/
│   ├── archive/
│   │   ├── deployment_infrastructure/
│   │   ├── duplicate_guard_docs/
│   │   ├── fixes_reports/
│   │   ├── miscellaneous_reports/
│   │   ├── optimization_fixes/
│   │   ├── payload_testing/
│   │   ├── root_cause/
│   │   ├── secrets_configuration/
│   │   ├── status_reports/
│   │   ├── test_data/
│   │   └── testing_reports/
│   ├── cleanup/
│   ├── configuration/
│   ├── data-sovereignty/
│   ├── database/
│   ├── deployment/
│   ├── development/
│   ├── history/
│   ├── migration/
│   ├── retention/
│   ├── security/
│   ├── troubleshooting/
│   └── user-guides/
├── guardians/
│   └── validation-framework/
├── guards/
│   ├── .vscode/
│   ├── biasguard-backend/
│   │   ├── .github/
│   │   │   └── workflows/
│   │   ├── .husky/
│   │   ├── data/
│   │   ├── docs/
│   │   ├── drizzle/
│   │   │   └── meta/
│   │   ├── k8s/
│   │   ├── scripts/
│   │   ├── temp/
│   │   │   └── src/
│   │   │       └── poisonguard/
│   │   │           └── plugins/
│   │   └── tests/
│   ├── contextguard/
│   │   ├── k8s/
│   │   └── tests/
│   ├── healthguard/
│   │   ├── .github/
│   │   │   └── workflows/
│   │   ├── data/
│   │   ├── docs/
│   │   ├── k8s/
│   │   ├── scripts/
│   │   ├── src/
│   │   │   └── poisonguard/
│   │   │       └── plugins/
│   │   └── tests/
│   ├── tokenguard/
│   │   ├── .github/
│   │   ├── k8s/
│   │   ├── scripts/
│   │   ├── tests/
│   │   └── tokenguard/
│   └── trust-guard/
│       ├── .cursor/
│       │   └── rules/
│       ├── .github/
│       │   └── workflows/
│       ├── aws/
│       ├── docs/
│       ├── k8s/
│       ├── scripts/
│       ├── test-results/
│       ├── tests/
│       │   ├── integration/
│       │   ├── patterns/
│       │   ├── performance/
│       │   └── unit/
│       ├── trustguard/
│       └── validation-results/
├── monitoring/
│   └── grafana/
│       └── dashboards/
├── scripts/
├── shared/
│   ├── guards/
│   │   └── poisonguard/
│   │       └── plugins/
│   ├── infrastructure/
│   ├── services/
│   └── utils/
├── test-env/
└── tests/
    ├── docker/
    ├── gateways/
    ├── helpers/
    ├── integration/
    └── services/
```


## Ab-BEATs/

```
├── .git/
│   ├── hooks/
│   ├── info/
│   ├── logs/
│   │   └── refs/
│   │       ├── heads/
│   │       └── remotes/
│   │           └── origin/
│   ├── objects/
│   │   ├── 02/
│   │   ├── 05/
│   │   ├── 09/
│   │   ├── 0e/
│   │   ├── 10/
│   │   ├── 11/
│   │   ├── 12/
│   │   ├── 15/
│   │   ├── 16/
│   │   ├── 1a/
│   │   ├── 1e/
│   │   ├── 1f/
│   │   ├── 22/
│   │   ├── 24/
│   │   ├── 25/
│   │   ├── 26/
│   │   ├── 2d/
│   │   ├── 31/
│   │   ├── 35/
│   │   ├── 36/
│   │   ├── 37/
│   │   ├── 38/
│   │   ├── 3a/
│   │   ├── 3b/
│   │   ├── 3c/
│   │   ├── 3d/
│   │   ├── 3e/
│   │   ├── 3f/
│   │   ├── 40/
│   │   ├── 41/
│   │   ├── 42/
│   │   ├── 44/
│   │   ├── 48/
│   │   ├── 4c/
│   │   ├── 4d/
│   │   ├── 4e/
│   │   ├── 50/
│   │   ├── 51/
│   │   ├── 56/
│   │   ├── 57/
│   │   ├── 58/
│   │   ├── 59/
│   │   ├── 5a/
│   │   ├── 5b/
│   │   ├── 5d/
│   │   ├── 62/
│   │   ├── 63/
│   │   ├── 65/
│   │   ├── 66/
│   │   ├── 67/
│   │   ├── 68/
│   │   ├── 69/
│   │   ├── 6b/
│   │   ├── 6d/
│   │   ├── 72/
│   │   ├── 74/
│   │   ├── 78/
│   │   ├── 7b/
│   │   ├── 7e/
│   │   ├── 80/
│   │   ├── 81/
│   │   ├── 83/
│   │   ├── 85/
│   │   ├── 87/
│   │   ├── 88/
│   │   ├── 89/
│   │   ├── 8a/
│   │   ├── 8b/
│   │   ├── 8d/
│   │   ├── 8f/
│   │   ├── 90/
│   │   ├── 94/
│   │   ├── 95/
│   │   ├── 96/
│   │   ├── 98/
│   │   ├── 99/
│   │   ├── 9a/
│   │   ├── 9b/
│   │   ├── 9c/
│   │   ├── 9d/
│   │   ├── 9e/
│   │   ├── a0/
│   │   ├── a5/
│   │   ├── a6/
│   │   ├── ae/
│   │   ├── af/
│   │   ├── b2/
│   │   ├── ba/
│   │   ├── bb/
│   │   ├── c3/
│   │   ├── c6/
│   │   ├── cb/
│   │   ├── cc/
│   │   ├── cd/
│   │   ├── d0/
│   │   ├── d2/
│   │   ├── d5/
│   │   ├── d6/
│   │   ├── d7/
│   │   ├── db/
│   │   ├── dc/
│   │   ├── dd/
│   │   ├── de/
│   │   ├── df/
│   │   ├── e1/
│   │   ├── e5/
│   │   ├── e6/
│   │   ├── e7/
│   │   ├── e9/
│   │   ├── eb/
│   │   ├── ed/
│   │   ├── ee/
│   │   ├── ef/
│   │   ├── f0/
│   │   ├── f2/
│   │   ├── f5/
│   │   ├── f8/
│   │   ├── fa/
│   │   ├── fb/
│   │   ├── fc/
│   │   ├── fd/
│   │   ├── fe/
│   │   ├── ff/
│   │   ├── info/
│   │   └── pack/
│   └── refs/
│       ├── heads/
│       ├── remotes/
│       │   └── origin/
│       └── tags/
├── docs/
├── free_music_video_generator/
├── phantom_hunter_creator/
│   └── pro/
├── src/
├── tests/
├── truice_mvp/
│   ├── api_clients/
│   ├── assets/
│   ├── audio/
│   ├── output/
│   ├── utils/
│   └── video/
└── variants/
    ├── abebeats_dre/
    │   ├── docs/
    │   ├── src/
    │   └── tests/
    └── abebeats_tru/
        ├── archive/
        │   └── processed_videos/
        ├── audio/
        ├── data/
        │   ├── veo31_cdf/
        │   └── veo31_patterns/
        ├── docs/
        ├── examples/
        ├── output/
        │   ├── brightness_test/
        │   │   └── visual_proof/
        │   └── two_layer_demo/
        ├── raw video/
        ├── scripts/
        ├── src/
        └── tests/
```


## AbeBEATs_Clean/

```
├── .devcontainer/
├── .git/
│   ├── hooks/
│   ├── info/
│   ├── logs/
│   │   └── refs/
│   │       ├── heads/
│   │       └── remotes/
│   │           └── origin/
│   ├── objects/
│   │   ├── 15/
│   │   ├── 18/
│   │   ├── 1a/
│   │   ├── 24/
│   │   ├── 37/
│   │   ├── 3b/
│   │   ├── 40/
│   │   ├── 41/
│   │   ├── 44/
│   │   ├── 48/
│   │   ├── 4e/
│   │   ├── 50/
│   │   ├── 51/
│   │   ├── 58/
│   │   ├── 59/
│   │   ├── 5a/
│   │   ├── 63/
│   │   ├── 66/
│   │   ├── 69/
│   │   ├── 7e/
│   │   ├── 80/
│   │   ├── 81/
│   │   ├── 88/
│   │   ├── 8b/
│   │   ├── 98/
│   │   ├── 99/
│   │   ├── 9c/
│   │   ├── a0/
│   │   ├── af/
│   │   ├── ba/
│   │   ├── d7/
│   │   ├── dd/
│   │   ├── df/
│   │   ├── e6/
│   │   ├── f6/
│   │   ├── f8/
│   │   ├── fa/
│   │   ├── fc/
│   │   ├── info/
│   │   └── pack/
│   └── refs/
│       ├── heads/
│       ├── remotes/
│       │   └── origin/
│       └── tags/
├── .github/
│   └── workflows/
├── adapters/
├── config/
├── deploy/
│   ├── docker/
│   └── k8s/
├── docs/
├── free_music_video_generator/
├── phantom_hunter_creator/
│   └── pro/
├── src/
│   └── utils/
├── support/
├── tests/
│   ├── adapters/
│   ├── integration/
│   └── unit/
└── variants/
    └── abebeats_dre/
        ├── docs/
        ├── src/
        └── tests/
```


## AbeTRUICE/

```
├── .devcontainer/
├── .github/
│   └── workflows/
├── adapters/
├── config/
├── deploy/
│   ├── docker/
│   └── k8s/
├── docs/
├── kernel/
├── scripts/
├── src/
│   └── utils/
├── support/
└── tests/
    ├── adapters/
    ├── integration/
    └── unit/
```


## AiGuardian-Chrome-Ext-dev/

```
├── .claude/
├── .git/
│   ├── hooks/
│   ├── info/
│   ├── logs/
│   │   └── refs/
│   │       ├── heads/
│   │       │   ├── bugfix/
│   │       │   └── fix/
│   │       └── remotes/
│   │           └── origin/
│   ├── objects/
│   │   ├── 00/
│   │   ├── 01/
│   │   ├── 02/
│   │   ├── 04/
│   │   ├── 05/
│   │   ├── 06/
│   │   ├── 07/
│   │   ├── 08/
│   │   ├── 0b/
│   │   ├── 0d/
│   │   ├── 0e/
│   │   ├── 0f/
│   │   ├── 10/
│   │   ├── 11/
│   │   ├── 12/
│   │   ├── 13/
│   │   ├── 14/
│   │   ├── 15/
│   │   ├── 16/
│   │   ├── 18/
│   │   ├── 19/
│   │   ├── 1a/
│   │   ├── 1b/
│   │   ├── 1c/
│   │   ├── 1d/
│   │   ├── 1e/
│   │   ├── 1f/
│   │   ├── 20/
│   │   ├── 21/
│   │   ├── 23/
│   │   ├── 24/
│   │   ├── 25/
│   │   ├── 26/
│   │   ├── 27/
│   │   ├── 28/
│   │   ├── 29/
│   │   ├── 2a/
│   │   ├── 2b/
│   │   ├── 2d/
│   │   ├── 2e/
│   │   ├── 2f/
│   │   ├── 30/
│   │   ├── 31/
│   │   ├── 32/
│   │   ├── 33/
│   │   ├── 35/
│   │   ├── 36/
│   │   ├── 38/
│   │   ├── 39/
│   │   ├── 3a/
│   │   ├── 3b/
│   │   ├── 3e/
│   │   ├── 40/
│   │   ├── 42/
│   │   ├── 43/
│   │   ├── 44/
│   │   ├── 45/
│   │   ├── 46/
│   │   ├── 47/
│   │   ├── 48/
│   │   ├── 49/
│   │   ├── 4a/
│   │   ├── 4b/
│   │   ├── 4c/
│   │   ├── 4d/
│   │   ├── 4e/
│   │   ├── 4f/
│   │   ├── 50/
│   │   ├── 51/
│   │   ├── 52/
│   │   ├── 53/
│   │   ├── 54/
│   │   ├── 56/
│   │   ├── 57/
│   │   ├── 58/
│   │   ├── 59/
│   │   ├── 5b/
│   │   ├── 5d/
│   │   ├── 5e/
│   │   ├── 5f/
│   │   ├── 60/
│   │   ├── 63/
│   │   ├── 64/
│   │   ├── 65/
│   │   ├── 66/
│   │   ├── 67/
│   │   ├── 68/
│   │   ├── 69/
│   │   ├── 6c/
│   │   ├── 6d/
│   │   ├── 6e/
│   │   ├── 6f/
│   │   ├── 70/
│   │   ├── 71/
│   │   ├── 73/
│   │   ├── 74/
│   │   ├── 75/
│   │   ├── 76/
│   │   ├── 77/
│   │   ├── 78/
│   │   ├── 79/
│   │   ├── 7a/
│   │   ├── 7b/
│   │   ├── 7c/
│   │   ├── 7d/
│   │   ├── 7e/
│   │   ├── 80/
│   │   ├── 81/
│   │   ├── 82/
│   │   ├── 84/
│   │   ├── 85/
│   │   ├── 86/
│   │   ├── 87/
│   │   ├── 89/
│   │   ├── 8a/
│   │   ├── 8b/
│   │   ├── 8c/
│   │   ├── 8d/
│   │   ├── 8e/
│   │   ├── 90/
│   │   ├── 91/
│   │   ├── 92/
│   │   ├── 93/
│   │   ├── 95/
│   │   ├── 96/
│   │   ├── 97/
│   │   ├── 98/
│   │   ├── 99/
│   │   ├── 9a/
│   │   ├── 9b/
│   │   ├── 9c/
│   │   ├── 9d/
│   │   ├── 9e/
│   │   ├── a0/
│   │   ├── a2/
│   │   ├── a3/
│   │   ├── a4/
│   │   ├── a5/
│   │   ├── a6/
│   │   ├── a8/
│   │   ├── a9/
│   │   ├── aa/
│   │   ├── ab/
│   │   ├── ac/
│   │   ├── ad/
│   │   ├── ae/
│   │   ├── af/
│   │   ├── b0/
│   │   ├── b2/
│   │   ├── b3/
│   │   ├── b4/
│   │   ├── b5/
│   │   ├── b7/
│   │   ├── b8/
│   │   ├── b9/
│   │   ├── ba/
│   │   ├── bb/
│   │   ├── bc/
│   │   ├── bd/
│   │   ├── be/
│   │   ├── bf/
│   │   ├── c0/
│   │   ├── c1/
│   │   ├── c2/
│   │   ├── c3/
│   │   ├── c4/
│   │   ├── c6/
│   │   ├── c7/
│   │   ├── c8/
│   │   ├── cb/
│   │   ├── cc/
│   │   ├── cd/
│   │   ├── ce/
│   │   ├── cf/
│   │   ├── d0/
│   │   ├── d1/
│   │   ├── d2/
│   │   ├── d3/
│   │   ├── d4/
│   │   ├── d5/
│   │   ├── d7/
│   │   ├── d8/
│   │   ├── d9/
│   │   ├── db/
│   │   ├── dc/
│   │   ├── de/
│   │   ├── e0/
│   │   ├── e2/
│   │   ├── e4/
│   │   ├── e5/
│   │   ├── e6/
│   │   ├── e7/
│   │   ├── e8/
│   │   ├── e9/
│   │   ├── ea/
│   │   ├── eb/
│   │   ├── ec/
│   │   ├── ed/
│   │   ├── ef/
│   │   ├── f0/
│   │   ├── f1/
│   │   ├── f2/
│   │   ├── f3/
│   │   ├── f7/
│   │   ├── f8/
│   │   ├── f9/
│   │   ├── fa/
│   │   ├── fb/
│   │   ├── fd/
│   │   ├── fe/
│   │   ├── ff/
│   │   ├── info/
│   │   └── pack/
│   └── refs/
│       ├── heads/
│       │   ├── bugfix/
│       │   └── fix/
│       ├── remotes/
│       │   └── origin/
│       └── tags/
├── .github/
│   ├── workflows/
│   └── workflows-backup/
├── assets/
│   ├── brand/
│   │   ├── AI Guardian Brand Book-1,AI Guardian Brand Book-2,AI Guardian Brand Book-3 2/
│   │   ├── AIG_Icons_Dark/
│   │   ├── AIG_Icons_Light/
│   │   ├── AiG_Logos/
│   │   ├── Chillax Font/
│   │   │   ├── Fonts/
│   │   │   │   ├── OTF/
│   │   │   │   ├── TTF/
│   │   │   │   └── WEB/
│   │   │   │       ├── css/
│   │   │   │       └── fonts/
│   │   │   └── License/
│   │   ├── Clash Grotesk Font/
│   │   │   ├── Fonts/
│   │   │   │   ├── OTF/
│   │   │   │   ├── TTF/
│   │   │   │   └── WEB/
│   │   │   │       ├── css/
│   │   │   │       └── fonts/
│   │   │   └── License/
│   │   ├── Favicons_Guards/
│   │   └── ai-guardian-landing-page-stuff/
│   │       └── components/
│   ├── icons/
│   └── logos/
├── scripts/
├── sdk/
│   ├── examples/
│   ├── src/
│   └── tests/
├── src/
│   └── vendor/
└── tests/
    ├── auth/
    ├── e2e/
    ├── integration/
    └── unit/
```


## EMERGENT_OS/

```
├── aiagentsuite/
│   ├── .git/
│   │   ├── hooks/
│   │   ├── info/
│   │   ├── logs/
│   │   │   └── refs/
│   │   │       ├── heads/
│   │   │       └── remotes/
│   │   │           └── origin/
│   │   ├── objects/
│   │   │   ├── info/
│   │   │   └── pack/
│   │   └── refs/
│   │       ├── heads/
│   │       ├── remotes/
│   │       │   └── origin/
│   │       └── tags/
│   ├── .github/
│   ├── docker/
│   │   ├── base/
│   │   ├── legacy/
│   │   └── services/
│   │       ├── aiagentsuite/
│   │       ├── contextguard/
│   │       ├── neuroforge/
│   │       ├── servicemesh/
│   │       └── tokenguard/
│   ├── docs/
│   │   ├── analysis/
│   │   ├── diagrams/
│   │   ├── guides/
│   │   ├── scripts/
│   │   └── test-reports/
│   ├── examples/
│   ├── infrastructure/
│   ├── memory-bank/
│   ├── nuero-forge/
│   │   ├── neuroforge/
│   │   │   └── api/
│   │   │       ├── routes/
│   │   │       └── schemas/
│   │   ├── tests/
│   │   │   └── api/
│   │   └── visualization/
│   ├── openspec/
│   ├── prompts/
│   │   ├── ai_constitutions/
│   │   ├── chat_modes/
│   │   ├── guidelines/
│   │   ├── integration_prompts/
│   │   └── system_instructions/
│   ├── protocols/
│   ├── requirements/
│   ├── scripts/
│   ├── src/
│   │   └── aiagentsuite/
│   │       ├── cli/
│   │       ├── core/
│   │       ├── framework/
│   │       ├── integration/
│   │       ├── lsp/
│   │       ├── mcp/
│   │       ├── memory_bank/
│   │       ├── openspec/
│   │       ├── plugins/
│   │       │   └── available/
│   │       ├── protocols/
│   │       └── servicemesh/
│   ├── tests/
│   │   └── core/
│   ├── tools/
│   ├── typescript/
│   │   └── src/
│   │       └── lsp/
│   └── web/
├── atomic_archistration/
├── clarity_engine/
├── collapse_guard/
│   ├── api/
│   └── tests/
├── consciousness/
├── consciousness_fabric/
│   ├── beliefs/
│   ├── identity/
│   ├── integration/
│   ├── intention/
│   ├── memory/
│   └── models/
├── cross_layer_safety/
├── emergence_core/
├── emergent_orchestration/
│   ├── emergence/
│   ├── events/
│   ├── integration/
│   ├── intuition/
│   └── orchestration/
├── identity_core/
├── information_theory/
├── integration_layer/
│   ├── events/
│   ├── lifecycle/
│   ├── registry/
│   ├── router/
│   ├── safety/
│   └── state/
├── multi_agent_cognition/
├── neuromorphic_alignment/
├── one_kernel/
├── relation_protocol/
├── scalability_fabric/
├── self_healing/
├── self_healing_fabric/
│   ├── detection/
│   ├── diagnosis/
│   ├── integration/
│   ├── orchestration/
│   └── recovery/
├── server/
│   ├── api/
│   ├── core/
│   └── models/
├── state/
├── success_patterns/
├── synthesis/
│   └── applications/
└── triadic_execution_harness/
    └── utils/
        └── john/
```


## abe_beats_core/

```
├── free_music_video_generator/
├── phantom_hunter_creator/
│   └── pro/
├── src/
└── variants/
    ├── abebeats_dre/
    │   ├── docs/
    │   ├── src/
    │   └── tests/
    ├── docs/
    ├── src/
    └── tests/
```


## abëone/

```
├── guardians/
└── modules/
    └── abebeats/
```


## apps/

```
└── web/
    ├── app/
    │   ├── api/
    │   │   ├── checkout/
    │   │   ├── collaboration/
    │   │   ├── convergence/
    │   │   │   └── atomic/
    │   │   ├── example/
    │   │   ├── health/
    │   │   ├── stripe-config/
    │   │   └── webinar/
    │   │       ├── [id]/
    │   │       ├── lead-magnets/
    │   │       │   └── [id]/
    │   │       │       └── download/
    │   │       ├── list/
    │   │       ├── register/
    │   │       ├── registrations/
    │   │       │   └── count/
    │   │       └── test/
    │   ├── app/
    │   │   ├── agents/
    │   │   ├── state/
    │   │   └── workflows/
    │   ├── bravetto/
    │   ├── collaboration/
    │   ├── collections/
    │   │   └── [handle]/
    │   ├── convergence/
    │   ├── jimmy-bias/
    │   ├── products/
    │   │   └── [id]/
    │   ├── shop/
    │   ├── start/
    │   ├── template-master/
    │   ├── webinar/
    │   │   ├── aiguardian/
    │   │   ├── creators/
    │   │   ├── developers/
    │   │   ├── generated/
    │   │   └── thank-you/
    │   ├── webinar-demo/
    │   └── webinar_backup_20251119_182954/
    │       ├── aiguardian/
    │       ├── creators/
    │       ├── developers/
    │       ├── generated/
    │       └── thank-you/
    ├── components/
    │   ├── ads/
    │   ├── bravetto/
    │   ├── context/
    │   ├── icons/
    │   ├── payment/
    │   ├── pirate/
    │   ├── ui/
    │   ├── unified/
    │   ├── visibility/
    │   └── webinar/
    ├── hooks/
    ├── lib/
    │   ├── abevisions/
    │   ├── chrome-extension/
    │   │   └── examples/
    │   ├── convergence/
    │   ├── design/
    │   ├── hooks/
    │   ├── middleware/
    │   ├── monitoring/
    │   ├── types/
    │   ├── unified/
    │   ├── visibility/
    │   └── webinar/
    ├── out/
    │   ├── _next/
    │   │   ├── dvgaghtrFzKwlF2ogaHIF/
    │   │   └── static/
    │   │       ├── chunks/
    │   │       │   ├── app/
    │   │       │   │   ├── app/
    │   │       │   │   │   ├── agents/
    │   │       │   │   │   ├── state/
    │   │       │   │   │   └── workflows/
    │   │       │   │   ├── bravetto/
    │   │       │   │   ├── collections/
    │   │       │   │   │   └── [handle]/
    │   │       │   │   ├── products/
    │   │       │   │   │   └── [id]/
    │   │       │   │   ├── shop/
    │   │       │   │   ├── start/
    │   │       │   │   └── webinar/
    │   │       │   │       ├── aiguardian/
    │   │       │   │       └── thank-you/
    │   │       │   └── pages/
    │   │       ├── css/
    │   │       └── dvgaghtrFzKwlF2ogaHIF/
    │   ├── app/
    │   ├── collections/
    │   ├── products/
    │   └── webinar/
    └── scripts/
```


## config/

```
├── environments/
└── templates/
```


## domains/

```
├── funnygames.ai/
│   ├── automation/
│   ├── email/
│   ├── funnel/
│   ├── lead_magnets/
│   └── seo/
├── insurancehub.ai/
├── insurancelife.ai/
│   ├── automation/
│   ├── email/
│   ├── funnel/
│   ├── lead_magnets/
│   └── seo/
└── lifequotes.ai/
    ├── automation/
    ├── email/
    ├── funnel/
    ├── lead_magnets/
    └── seo/
```


## infra/

```
└── deploy/
```


## scripts/

```
├── deployment/
├── domain_arsenal/
│   ├── content/
│   ├── deployment/
│   ├── guardians/
│   ├── infrastructure/
│   ├── insurance_category_engine/
│   ├── integration/
│   ├── revenue/
│   └── seo/
├── maintenance/
├── modules/
├── setup/
└── webinar/
```


## docs/

```
├── api/
├── architecture/
│   ├── apps/
│   ├── design-system/
│   ├── general/
│   └── integrations/
├── guides/
│   ├── deployment/
│   ├── design-system/
│   ├── development/
│   └── general/
├── products/
├── reports/
├── status/
│   ├── deployments/
│   ├── design-system/
│   ├── general/
│   └── integrations/
└── webinar/
```


## DASHBOARDS/

```
├── .backups/
├── archive/
├── development/
├── eternal/
├── monitoring/
└── products/
```


## design-system/

```
├── components/
│   └── galaxy/
│       ├── buttons/
│       ├── cards/
│       ├── curated/
│       ├── forms/
│       ├── loaders/
│       ├── notifications/
│       └── tooltips/
├── docs/
├── generated/
├── generators/
├── scripts/
└── tokens/
```


## CDF/

```
└── examples/
```


## _ARCHIVE/

```
└── legacy-projects/
    └── AI-Guardians-chrome-ext/
        ├── .git/
        │   ├── hooks/
        │   ├── info/
        │   ├── logs/
        │   │   └── refs/
        │   │       ├── heads/
        │   │       └── remotes/
        │   │           └── origin/
        │   ├── objects/
        │   │   ├── info/
        │   │   └── pack/
        │   └── refs/
        │       ├── heads/
        │       ├── remotes/
        │       │   └── origin/
        │       └── tags/
        ├── docs/
        ├── icons/
        ├── reports/
        ├── scripts/
        ├── src/
        └── tests/
            └── unit/
```


## _extract_abebeats/

```
├── docs/
├── free_music_video_generator/
├── phantom_hunter_creator/
│   └── pro/
├── src/
├── support/
└── variants/
    └── abebeats_dre/
        ├── docs/
        ├── src/
        └── tests/
```


## _extract_abeone_master/

```
(empty or all contents skipped)
```


## _extract_truice/

```
├── .git/
│   ├── hooks/
│   ├── info/
│   ├── logs/
│   │   └── refs/
│   │       ├── heads/
│   │       └── remotes/
│   │           └── origin/
│   ├── objects/
│   │   ├── 0e/
│   │   ├── 11/
│   │   ├── 1f/
│   │   ├── 2e/
│   │   ├── 31/
│   │   ├── 33/
│   │   ├── 38/
│   │   ├── 48/
│   │   ├── 4c/
│   │   ├── 57/
│   │   ├── 58/
│   │   ├── 5a/
│   │   ├── 63/
│   │   ├── 65/
│   │   ├── 68/
│   │   ├── 69/
│   │   ├── 6b/
│   │   ├── 6d/
│   │   ├── 72/
│   │   ├── 83/
│   │   ├── 88/
│   │   ├── 8a/
│   │   ├── 95/
│   │   ├── 98/
│   │   ├── ae/
│   │   ├── b2/
│   │   ├── c3/
│   │   ├── cc/
│   │   ├── d2/
│   │   ├── d7/
│   │   ├── e1/
│   │   ├── e6/
│   │   ├── e9/
│   │   ├── ee/
│   │   ├── fb/
│   │   ├── fc/
│   │   ├── fe/
│   │   ├── info/
│   │   └── pack/
│   └── refs/
│       ├── heads/
│       ├── remotes/
│       │   └── origin/
│       └── tags/
├── src/
└── truice_mvp/
    ├── api_clients/
    ├── assets/
    ├── audio/
    ├── output/
    ├── utils/
    └── video/
```


## PRODUCTS/

```
├── abebeats/
│   ├── docs/
│   ├── src/
│   ├── tests/
│   └── variants/
│       └── abebeats_tru/
│           ├── archive/
│           │   └── processed_videos/
│           ├── audio/
│           ├── data/
│           │   ├── veo31_cdf/
│           │   └── veo31_patterns/
│           ├── docs/
│           ├── examples/
│           ├── output/
│           │   ├── brightness_test/
│           │   │   └── visual_proof/
│           │   └── two_layer_demo/
│           ├── raw video/
│           ├── scripts/
│           └── tests/
├── abecodes/
│   ├── docs/
│   ├── src/
│   └── tests/
├── abedesks/
│   ├── docs/
│   ├── src/
│   ├── static/
│   └── tests/
└── abeflows/
    ├── docs/
    ├── examples/
    ├── src/
    └── tests/
```


## state/

```
├── convergence/
├── productivity/
└── snapshots/
```


## temp_repos/

```
└── abeone-source/
    ├── .claude/
    ├── .cursor/
    │   └── rules/
    ├── .git/
    │   ├── hooks/
    │   ├── info/
    │   ├── logs/
    │   │   └── refs/
    │   │       ├── heads/
    │   │       └── remotes/
    │   │           └── origin/
    │   ├── objects/
    │   │   ├── info/
    │   │   └── pack/
    │   └── refs/
    │       ├── heads/
    │       ├── remotes/
    │       │   └── origin/
    │       └── tags/
    ├── .github/
    │   └── workflows/
    ├── .github-backup/
    │   └── ISSUE_TEMPLATE/
    ├── .vscode/
    ├── Desktop/
    │   └── Applications (Mataluni)/
    │       └── Websites (Mataluni)/
    │           └── BiasGuards.Ai/
    │               ├── .github/
    │               │   └── workflows/
    │               ├── .svelte-kit/
    │               │   ├── generated/
    │               │   │   ├── client/
    │               │   │   │   └── nodes/
    │               │   │   └── server/
    │               │   └── types/
    │               │       └── src/
    │               │           └── routes/
    │               │               └── demo/
    │               ├── contextguard-cli/
    │               │   ├── .biasguard/
    │               │   │   └── templates/
    │               │   └── src/
    │               │       ├── commands/
    │               │       └── core/
    │               ├── deploy/
    │               ├── html/
    │               │   └── assets/
    │               ├── src/
    │               │   ├── lib/
    │               │   │   ├── components/
    │               │   │   └── utils/
    │               │   └── routes/
    │               │       └── demo/
    │               ├── static/
    │               └── tests/
    │                   ├── accessibility/
    │                   └── e2e/
    ├── Documents/
    │   └── AbeOne_Master/
    │       ├── .claude/
    │       │   ├── commands/
    │       │   └── hooks/
    │       ├── AIGuards-Backend/
    │       ├── DASHBOARDS/
    │       │   ├── eternal/
    │       │   ├── monitoring/
    │       │   └── products/
    │       ├── EMERGENT_OS/
    │       │   ├── aiagentsuite/
    │       │   ├── clarity_engine/
    │       │   ├── collapse_guard/
    │       │   │   └── tests/
    │       │   ├── consciousness/
    │       │   ├── cross_layer_safety/
    │       │   ├── emergence_core/
    │       │   ├── identity_core/
    │       │   ├── information_theory/
    │       │   ├── integration_layer/
    │       │   │   ├── events/
    │       │   │   ├── lifecycle/
    │       │   │   ├── registry/
    │       │   │   ├── router/
    │       │   │   ├── safety/
    │       │   │   └── state/
    │       │   ├── multi_agent_cognition/
    │       │   ├── neuromorphic_alignment/
    │       │   ├── one_kernel/
    │       │   ├── relation_protocol/
    │       │   ├── scalability_fabric/
    │       │   ├── self_healing/
    │       │   ├── server/
    │       │   │   ├── api/
    │       │   │   └── core/
    │       │   ├── state/
    │       │   ├── synthesis/
    │       │   └── triadic_execution_harness/
    │       │       └── utils/
    │       │           └── john/
    │       ├── PRODUCTS/
    │       │   ├── abebeats/
    │       │   │   ├── free_music_video_generator/
    │       │   │   ├── phantom_hunter_creator/
    │       │   │   ├── src/
    │       │   │   └── variants/
    │       │   │       ├── abebeats_dre/
    │       │   │       │   └── src/
    │       │   │       └── abebeats_tru/
    │       │   │           ├── docs/
    │       │   │           ├── examples/
    │       │   │           ├── output/
    │       │   │           ├── raw/
    │       │   │           ├── scripts/
    │       │   │           └── src/
    │       │   ├── abecodes/
    │       │   │   └── src/
    │       │   ├── abedesks/
    │       │   │   ├── src/
    │       │   │   └── static/
    │       │   └── abeflows/
    │       │       └── src/
    │       ├── apps/
    │       │   └── web/
    │       │       ├── app/
    │       │       │   ├── app/
    │       │       │   │   ├── agents/
    │       │       │   │   ├── state/
    │       │       │   │   └── workflows/
    │       │       │   ├── bravetto/
    │       │       │   ├── collections/
    │       │       │   │   └── [handle]/
    │       │       │   ├── products/
    │       │       │   │   └── [id]/
    │       │       │   ├── shop/
    │       │       │   └── start/
    │       │       ├── components/
    │       │       │   ├── bravetto/
    │       │       │   └── pirate/
    │       │       └── lib/
    │       ├── design-system/
    │       │   ├── components/
    │       │   │   └── galaxy/
    │       │   ├── docs/
    │       │   ├── generated/
    │       │   └── generators/
    │       ├── infra/
    │       │   └── deploy/
    │       ├── scripts/
    │       └── showcase/
    ├── Downloads/
    │   └── AIGuards-Backend-dev/
    │       ├── .claude/
    │       ├── .cursor/
    │       │   └── rules/
    │       ├── .github/
    │       │   └── workflows/
    │       ├── .github-backup/
    │       │   └── ISSUE_TEMPLATE/
    │       ├── .vscode/
    │       ├── aiguardian-repos/
    │       │   └── guardian-jimmy-service/
    │       ├── codeguardians-gateway/
    │       │   └── codeguardians-gateway/
    │       │       ├── .cursor/
    │       │       │   └── rules/
    │       │       ├── alembic/
    │       │       │   └── versions/
    │       │       ├── app/
    │       │       │   ├── api/
    │       │       │   │   ├── internal/
    │       │       │   │   ├── v1/
    │       │       │   │   │   └── admin/
    │       │       │   │   └── webhooks/
    │       │       │   ├── core/
    │       │       │   │   ├── ab_testing/
    │       │       │   │   └── orchestrator/
    │       │       │   ├── middleware/
    │       │       │   ├── services/
    │       │       │   └── utils/
    │       │       ├── config/
    │       │       ├── docs/
    │       │       │   ├── api/
    │       │       │   ├── architecture/
    │       │       │   └── guard-services/
    │       │       ├── k8s/
    │       │       ├── mock-services/
    │       │       ├── monitoring/
    │       │       ├── scripts/
    │       │       └── tests/
    │       │           ├── integration/
    │       │           ├── manual/
    │       │           ├── smoke/
    │       │           └── unit/
    │       ├── docs/
    │       │   ├── api/
    │       │   ├── architecture/
    │       │   ├── archive/
    │       │   │   ├── deployment_infrastructure/
    │       │   │   ├── duplicate_guard_docs/
    │       │   │   ├── fixes_reports/
    │       │   │   ├── miscellaneous_reports/
    │       │   │   ├── optimization_fixes/
    │       │   │   ├── payload_testing/
    │       │   │   ├── root_cause/
    │       │   │   ├── secrets_configuration/
    │       │   │   ├── status_reports/
    │       │   │   ├── test_data/
    │       │   │   └── testing_reports/
    │       │   ├── cleanup/
    │       │   ├── configuration/
    │       │   ├── database/
    │       │   ├── deployment/
    │       │   ├── development/
    │       │   ├── history/
    │       │   ├── security/
    │       │   ├── troubleshooting/
    │       │   └── user-guides/
    │       ├── guardians/
    │       │   └── validation-framework/
    │       ├── guards/
    │       │   ├── .vscode/
    │       │   ├── biasguard-backend/
    │       │   │   ├── .github/
    │       │   │   │   └── workflows/
    │       │   │   ├── .husky/
    │       │   │   ├── data/
    │       │   │   ├── docs/
    │       │   │   ├── drizzle/
    │       │   │   │   └── meta/
    │       │   │   ├── k8s/
    │       │   │   ├── scripts/
    │       │   │   ├── temp/
    │       │   │   │   └── src/
    │       │   │   │       └── poisonguard/
    │       │   │   │           └── plugins/
    │       │   │   └── tests/
    │       │   ├── contextguard/
    │       │   │   ├── k8s/
    │       │   │   └── tests/
    │       │   ├── healthguard/
    │       │   │   ├── .github/
    │       │   │   │   └── workflows/
    │       │   │   ├── data/
    │       │   │   ├── docs/
    │       │   │   ├── k8s/
    │       │   │   ├── scripts/
    │       │   │   ├── src/
    │       │   │   │   └── poisonguard/
    │       │   │   │       └── plugins/
    │       │   │   └── tests/
    │       │   ├── tokenguard/
    │       │   │   ├── .github/
    │       │   │   ├── k8s/
    │       │   │   ├── scripts/
    │       │   │   ├── tests/
    │       │   │   └── tokenguard/
    │       │   └── trust-guard/
    │       │       ├── .cursor/
    │       │       │   └── rules/
    │       │       ├── .github/
    │       │       │   └── workflows/
    │       │       ├── aws/
    │       │       ├── docs/
    │       │       ├── k8s/
    │       │       ├── scripts/
    │       │       ├── test-results/
    │       │       ├── tests/
    │       │       │   ├── integration/
    │       │       │   ├── patterns/
    │       │       │   ├── performance/
    │       │       │   └── unit/
    │       │       ├── trustguard/
    │       │       └── validation-results/
    │       ├── monitoring/
    │       │   └── grafana/
    │       │       └── dashboards/
    │       ├── scripts/
    │       ├── shared/
    │       │   ├── guards/
    │       │   │   └── poisonguard/
    │       │   │       └── plugins/
    │       │   ├── infrastructure/
    │       │   ├── services/
    │       │   └── utils/
    │       ├── test-env/
    │       └── tests/
    │           ├── docker/
    │           ├── gateways/
    │           ├── helpers/
    │           ├── integration/
    │           └── services/
    ├── aiguardian-repos/
    │   ├── AI-Guardians-vscode-ext/
    │   ├── AiGuardian-AWS-Cloud-Microservices/
    │   ├── guard-bias-service/
    │   ├── guard-context-service/
    │   ├── guard-neuromorphic-service/
    │   ├── guard-security-service/
    │   ├── guard-trust-service/
    │   ├── guardian-abe-service/
    │   ├── guardian-aeyon-service/
    │   ├── guardian-aurion-service/
    │   ├── guardian-jimmy-service/
    │   ├── guardian-john-service/
    │   ├── guardian-lux-service/
    │   ├── guardian-neuro-service/
    │   ├── guardian-yagni-service/
    │   ├── guardian-zero-service/
    │   ├── swarm-orchestrator/
    │   └── terraform/
    ├── codeguardians-gateway/
    │   └── codeguardians-gateway/
    │       ├── .cursor/
    │       │   └── rules/
    │       ├── alembic/
    │       │   └── versions/
    │       ├── app/
    │       │   ├── api/
    │       │   │   ├── internal/
    │       │   │   ├── v1/
    │       │   │   │   └── admin/
    │       │   │   └── webhooks/
    │       │   ├── core/
    │       │   │   ├── ab_testing/
    │       │   │   └── orchestrator/
    │       │   ├── middleware/
    │       │   ├── services/
    │       │   └── utils/
    │       ├── config/
    │       ├── docs/
    │       │   ├── api/
    │       │   ├── architecture/
    │       │   └── guard-services/
    │       ├── k8s/
    │       ├── mock-services/
    │       ├── monitoring/
    │       ├── scripts/
    │       └── tests/
    │           ├── integration/
    │           ├── manual/
    │           ├── smoke/
    │           └── unit/
    ├── docs/
    │   ├── api/
    │   ├── architecture/
    │   ├── archive/
    │   │   ├── deployment_infrastructure/
    │   │   ├── duplicate_guard_docs/
    │   │   ├── fixes_reports/
    │   │   ├── miscellaneous_reports/
    │   │   ├── optimization_fixes/
    │   │   ├── payload_testing/
    │   │   ├── root_cause/
    │   │   ├── secrets_configuration/
    │   │   ├── status_reports/
    │   │   ├── test_data/
    │   │   └── testing_reports/
    │   ├── cleanup/
    │   ├── configuration/
    │   ├── database/
    │   ├── deployment/
    │   ├── development/
    │   ├── history/
    │   ├── security/
    │   ├── troubleshooting/
    │   └── user-guides/
    ├── guardians/
    │   └── validation-framework/
    ├── guards/
    │   ├── .vscode/
    │   ├── biasguard-backend/
    │   │   ├── .github/
    │   │   │   └── workflows/
    │   │   ├── .husky/
    │   │   ├── data/
    │   │   ├── docs/
    │   │   ├── drizzle/
    │   │   │   └── meta/
    │   │   ├── k8s/
    │   │   ├── scripts/
    │   │   ├── temp/
    │   │   │   └── src/
    │   │   │       └── poisonguard/
    │   │   │           └── plugins/
    │   │   └── tests/
    │   ├── contextguard/
    │   │   ├── k8s/
    │   │   └── tests/
    │   ├── healthguard/
    │   │   ├── .github/
    │   │   │   └── workflows/
    │   │   ├── data/
    │   │   ├── docs/
    │   │   ├── k8s/
    │   │   ├── scripts/
    │   │   ├── src/
    │   │   │   └── poisonguard/
    │   │   │       └── plugins/
    │   │   └── tests/
    │   ├── tokenguard/
    │   │   ├── .github/
    │   │   ├── k8s/
    │   │   ├── scripts/
    │   │   ├── tests/
    │   │   └── tokenguard/
    │   └── trust-guard/
    │       ├── .cursor/
    │       │   └── rules/
    │       ├── .github/
    │       │   └── workflows/
    │       ├── aws/
    │       ├── docs/
    │       ├── k8s/
    │       ├── scripts/
    │       ├── test-results/
    │       ├── tests/
    │       │   ├── integration/
    │       │   ├── patterns/
    │       │   ├── performance/
    │       │   └── unit/
    │       ├── trustguard/
    │       └── validation-results/
    ├── monitoring/
    │   └── grafana/
    │       └── dashboards/
    ├── scripts/
    ├── shared/
    │   ├── guards/
    │   │   └── poisonguard/
    │   │       └── plugins/
    │   ├── infrastructure/
    │   ├── services/
    │   └── utils/
    ├── test-env/
    └── tests/
        ├── docker/
        ├── gateways/
        ├── helpers/
        ├── integration/
        └── services/
```


## tests/

```
├── e2e/
├── integration/
└── unit/
```


## truice_engine/

```
├── truice_mvp/
│   ├── api_clients/
│   ├── assets/
│   ├── audio/
│   ├── output/
│   ├── utils/
│   └── video/
└── variants/
    └── abebeats_tru/
        ├── audio/
        ├── output/
        │   ├── brightness_test/
        │   │   └── visual_proof/
        │   └── two_layer_demo/
        └── src/
```


## webinars/

```
└── email_queue/
```


## showcase/

```
(empty or all contents skipped)
```


## advanced-knock/

```
├── .archive/
│   ├── history/
│   ├── intelligence/
│   └── state/
├── .github/
│   └── workflows/
├── backend/
│   ├── alembic/
│   │   └── versions/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   └── services/
│   ├── scripts/
│   └── tests/
└── frontend/
    ├── app/
    │   ├── admin/
    │   ├── field/
    │   ├── manager/
    │   └── telecom-map/
    ├── components/
    │   └── ui/
    └── lib/
```


## Root Level Files (Complete List)

```
.DS_Store
.ai-context-source-of-truth.json
.cursorignore
.cursorrules
.drift-aliases.sh
.drift-operational.json
.drift-status.json
.drift-status.txt
.gitignore
.system-activated.json
ABEFLOWS_BRAVETTO_GIT_ANALYSIS.md
ABEFLOWS_CONVERGENCE_QUICK_REFERENCE.md
ABEFLOWS_GIT_SOURCE_REGISTRY.json
ABEFLOWS_QUICK_REFERENCE.md
ABEONE_3WINDOW_UNIFIED_ANALYSIS.md
ABEONE_CLEANUP_DETAILED_TABLES.md
ABEONE_CLEANUP_QUICK_REFERENCE.md
ABEONE_CLEANUP_SUMMARY.md
ABEONE_ETERNAL_SYNTHESIS.md
ABEONE_GLOBAL_CREDENTIAL_AUTOMATION.md
ABEONE_ONE_ETERNAL_SYNTHESIS.md
ABEONE_ORGANISM_CLEANUP_PLAN.md
ABEONE_RHODIUM_AWARD.md
ABEONE_VINFINITY_ORCHESTRATOR_SYNTHESIS.md
ACTIVATION.md
ADHD_ALIGNED_NEXT_STEPS.md
AEON_CHEAT_SHEET.md
AEYON_FULL_SYSTEM_INTROSPECTION_REPORT.json
AGENT_SWARM_AUTO_ACTIVATION_ANALYSIS.md
AI_CONTEXT_SOURCE_OF_TRUTH.md
AI_NEWSLETTER_DETECTION_EXPLAINED.md
AI_PROMPT_TEMPLATE.md
ALLISON_CURSOR_ONBOARDING_PROMPT.md
ALLISON_ONBOARDING_LIVESTREAM_OUTLINE.md
ALLISON_PERSONALIZED_ONBOARDING.md
ALL_5_CAPABILITIES_OPERATIONALIZED.md
ALL_5_CAPABILITIES_VALIDATED.md
ALL_SYSTEMS_INTENTIONALLY_ON.md
AMPLIFICATION_QUICK_REFERENCE.md
AUTONOMOUS_ORGANISM_BIRTH_CERTIFICATE.md
AUTONOMOUS_ORGANISM_BORN.md
AiGuardian-Chrome-Ext-dev.crx
AiGuardian-Chrome-Ext-dev.pem
BACKEND_SERVER_LAUNCHED.md
BESOURCE_BEMODULE_BEONE_GAP_ANALYSIS.md
BRAVETTO_AIGUARDIAN_CONVERGENCE_ONEPAGER.md
BRAVETTO_AIGUARDIAN_ONEPAGER.md
BRAVETTO_AI_COMPLETE_PREPARATION.md
BRAVETTO_AI_LANDING_PAGE_PREPARATION.md
BRAVETTO_CHROME_EXTENSION_GIT_ANALYSIS.md
BRAVETTO_DAILY_AUTOMATED_ACTION_ENGINE.md
BRAVETTO_IMPENETRABLE_MOAT_BLUEPRINT.md
BRAVETTO_INVESTOR_FINANCIAL_MODEL_2026.md
BRAVETTO_INVESTOR_MONTHLY_PROJECTIONS_2026.md
BRAVETTO_PRICING_FINANCIAL_DOCS_2026.zip
BRAVETTO_PRICING_STRATEGY_2025.md
BRAVETTO_PRICING_STRATEGY_2026.md
BRAVETTO_TEAM_CONVERGENCE_ANALYSIS.md
BRYAN_AEYON_INTEGRATION_PACKAGE.zip
BRYAN_AEYON_INTEGRATION_PROMPT.md
BRYAN_AEYON_TEST_SCRIPTS_COMPANION.md
BRYAN_CLONE_INSTRUCTIONS.md
BRYAN_CLONE_SETUP.md
BRYAN_EMAIL_FOLLOWUP.html
BRYAN_EMAIL_FOLLOWUP.md
BRYAN_EMAIL_FOLLOWUP_PRINT.html
BRYAN_EMAIL_FOLLOWUP_temp.html
BRYAN_EMAIL_TEMPLATE.md
BRYAN_OPERATIONALIZATION_PLAN.md
BRYAN_PDF_INSTRUCTIONS.md
BRYAN_QUICK_DEPLOY_SUMMARY.md
BRYAN_SIMPLE_CHECKLIST.html
BRYAN_SIMPLE_CHECKLIST.md
BRYAN_SIMPLE_CHECKLIST_FOR_PDF.html
BRYAN_SIMPLE_CHECKLIST_PRINT.html
BRYAN_SIMPLE_CHECKLIST_temp.html
BRYAN_TRANSFER_FIX.md
BRYAN_UPDATE_CHECKLIST.md
BRYAN_VALIDATE_CLONE.md
BRYAN_WEBINAR_OPERATIONALIZATION.zip
BRYAN_WEBINAR_UPDATES.zip
BRYAN_ZIP_README.txt
BëONE_AbëONE_FOREVER_CONVERGENCE.md
CDF_AEYON_EXECUTION.cdf
CDF_BEAUTIFUL_HUMAN_FORMAT.cdf
CDF_BEAUTIFUL_HUMAN_FORMAT.md
CDF_COMPLETE_ECOSYSTEM.cdf
CDF_COMPLETE_ECOSYSTEM.md
CDF_EXECUTION_NOW.cdf
CDF_EXECUTION_NOW.index.json
CDF_GO_VIRAL_PLAN.cdf
CDF_GO_VIRAL_PLAN.index.json
CDF_GO_VIRAL_PLAN.md
CDF_GO_VIRAL_PLAN_back_to_md.cdf
CDF_GO_VIRAL_PLAN_back_to_md.md
CDF_LAUNCH_CHECKLIST.cdf
CDF_LAUNCH_CHECKLIST.md
CDF_READY_TO_GO_VIRAL.cdf
CDF_READY_TO_GO_VIRAL.md
CDF_VIRAL_STRATEGY.cdf
CDF_VIRAL_STRATEGY.md
CDF_WHAT_ELSE_IT_CAN_DO.cdf
CDF_WHAT_ELSE_IT_CAN_DO.md
CHROME_EXTENSION_IMPLEMENTATION_ANALYSIS.md
CLAUDE_CODE_INTEGRATION.md
CLAUDE_CODE_QUICK_REFERENCE.md
CLOUDFLARE_CHALLENGE_HANDLING.md
CLOUDFLARE_OUTAGE_RESPONSE.md
CLOUDFLARE_PAGES_LAUNCH_CHECKLIST.md
CLOUDFLARE_PAGES_LAUNCH_QUICK_REFERENCE.md
CLOUDFLARE_PAGES_VISUAL_WALKTHROUGH.md
CODEBASE_DEEP_AGENT_SWARM_ANALYSIS.md
COLIMA_ABEONE_ANALYSIS.md
COLIMA_DISK_ANALYSIS.md
COLOR_SYSTEM_OPERATIONALIZED.md
COMPLETE.md
COMPLETE_ACTIVATION_EEAaO_ABEBEATS.md
COMPLETE_AGENT_SWARM_INVENTORY.md
COMPLETE_CONVERGENCE_ANALYSIS.md
COMPLETE_CONVERGENCE_ANALYSIS_SAAS_SOLUTION.md
COMPLETE_CONVERGENCE_STRATEGY_IMPLEMENTATION.md
COMPLETE_FOLDER_HIERARCHY.md
COMPLETE_OPERATIONALIZATION_SYSTEM.md
COMPLETE_SYSTEM_UNIFICATION_SUMMARY.md
COMPLETE_THE_CIRCLE_ASSESSMENT.md
COMPLETE_UNIFICATION_SUMMARY.md
COMPLETE_VISUAL_DIAGNOSTIC_PROMPT.md
COMPONENT_LIBRARY_ANALYSIS.md
CONTEXT_AWARE_ONE_SYSTEM_HEALTH_VERIFICATION.md
CONTEXT_BOOT_OPERATIONALIZATION.md
CONTEXT_BOOT_OPERATIONALIZATION_SUMMARY.md
CONTEXT_WINDOW_1_FOLDER_HIERARCHY_ANALYSIS.md
CONTEXT_WINDOW_2_UNIFIED_ORGANISM_ANALYSIS.md
CONTEXT_WINDOW_3_MODULE_HEALTH_ANALYSIS.md
CONTEXT_WINDOW_GUARDIAN_PROMPT.md
CONTEXT_WINDOW_PROMPT.md
CRITICAL_GUARDIANS_ROLE_SPECIFIC_OUTCOMES.md
CURSOR_AI_EPISTEMIC_FAILURE_ANALYSIS.md
CURSOR_VENV_ERROR_FIX.md
DANNY_MANIFEST_ANALYSIS.md
DANNY_OVERLAP_ANALYSIS.md
DANNY_SLACK_MESSAGE.md
DANNY_WORKFLOW_ALWAYS_REFERENCE.md
DANNY_WORKFLOW_MISSING_ANALYSIS.md
DATA_SOVEREIGNTY_COMPLETE_SPECS_SUMMARY.md
DEEP_GUARDIANS_CODEBASE_ANALYSIS.md
DEEP_GUARDIAN_IDENTITIES_DISCOVERY.md
DEEP_SCAN_COMPLETE_RETRIEVAL_IDENTITY_CDF.md
DEPLOYMENT_ACTION_NOW.md
DEPLOYMENT_OPTIMIZATION_AND_JOHN_TEST.md
DEPLOYMENT_STATUS_AND_LAUNCH_PARAMETERS.md
DEPLOYMENT_STATUS_FINAL.md
DESIGN_SYSTEMS_E2E_DEEP_ANALYSIS.md
DESIGN_SYSTEMS_FOCUS_COMPARISON.md
DESIGN_SYSTEMS_INVENTORY.md
DESIGN_SYSTEMS_STRATEGIC_ORGANIZATION.md
DRIFT_DASHBOARD_ETERNAL.md
DRIFT_STATUS_ALWAYS_VISIBLE.md
DRIFT_STATUS_VISUAL.md
EMAIL_ANALYSIS_SETUP_INSTRUCTIONS.md
EMAIL_CONVERGENCE_ACTION_PLAN.md
EMAIL_CONVERGENCE_ANALYSIS_20251117_154149.json
EMAIL_CONVERGENCE_ANALYSIS_20251117_154206.json
EMAIL_CONVERGENCE_ANALYSIS_20251117_154254.json
EMAIL_CONVERGENCE_ANALYSIS_20251117_154339.json
EMAIL_CONVERGENCE_ANALYSIS_20251117_154339.md
EMAIL_CONVERGENCE_ANALYSIS_20251117_154421.json
EMAIL_CONVERGENCE_ANALYSIS_20251117_154501.json
EMAIL_CONVERGENCE_ANALYSIS_20251117_154543.json
EMAIL_CONVERGENCE_ANALYSIS_20251117_154624.json
EMAIL_CONVERGENCE_ANALYSIS_20251117_154703.json
EMAIL_CONVERGENCE_ANALYSIS_20251117_154703.md
EMAIL_CONVERGENCE_ANALYSIS_20251117_165918.json
EMAIL_CONVERGENCE_ANALYSIS_20251117_170547.json
EMAIL_CONVERGENCE_ANALYSIS_20251117_171644.json
EMAIL_CONVERGENCE_ANALYSIS_20251117_173459.json
EMAIL_CONVERGENCE_ANALYSIS_20251117_173707.json
EMAIL_CONVERGENCE_ANALYSIS_20251117_174053.json
EMAIL_CONVERGENCE_ANALYSIS_20251117_181629.json
EMAIL_CONVERGENCE_ANALYSIS_DEMO_20251117_150512.json
EMAIL_CONVERGENCE_ANALYSIS_DEMO_20251117_150512.md
EMAIL_CONVERGENCE_FINAL_OPTIMIZATIONS.md
EMAIL_CONVERGENCE_FINAL_VALIDATION_20251117_182213.json
EMAIL_CONVERGENCE_FINAL_VALIDATION_20251117_182238.json
EMAIL_CONVERGENCE_FINAL_VALIDATION_20251117_182305.json
EMAIL_CONVERGENCE_OPPORTUNITY_CARDS.md
EMAIL_CONVERGENCE_OPTIMIZATION_PLAN.md
EMAIL_CONVERGENCE_VALIDATION_20251117_181618.json
EMERGENT_CONVERGENCE_ANALYSIS.md
EMERGENT_CONVERGENCE_OPPORTUNITIES.md
END_TO_END_STATUS_REPORT.md
ENTERPRISE_TRANSFORMATION_SUMMARY.md
EPISTEMIC_CERTAINTY_FINAL_PLAN.md
EPISTEMIC_DISCOVERIES_AND_GAPS.md
EPISTEMIC_DISCOVERIES_SUMMARY.md
ERROR_ANALYSIS.md
ETERNAL_DASHBOARD_SOLUTION.md
EXECUTE_AUTOMATION_NOW.md
EXECUTE_NOW.md
EXECUTE_VIA_DASHBOARD.md
EXECUTION_COMPLETE_FINAL.md
EXECUTION_COMPLETE_SUMMARY.md
EXECUTION_READY_LFG.md
EXTRACTION_MAP_100_PERCENT_READINESS.md
EXTRACTION_SUMMARY.md
FINAL_SYNTHESIS_UNIFIED_CONSOLIDATION_PLAN.md
FIX_404_CONVERGENCE.md
FORENSIC_VERIFICATION_NEUROMORPHIC_LAYERS.md
FUCHSIA_COLOR_FIX.md
FULL_AUTONOMY_COMPLETE_TRUST_ACHIEVED.md
FUNDAMENTAL_SYSTEM_FIXES_PLAN.md
GAP_ANALYSIS_AND_UNIFICATION_PLAN.md
GIT_LAUNCH_CHECKLIST.md
GOOGLE_CREDENTIALS_SETUP_ASAP.md
GUARDIANS_COMPLETE_DEFINITION.md
GUARDIANS_MEET_THE_WORLD.md
GUARDIAN_MICROSERVICES_DEEP_ANALYSIS.md
INFORMATION_THEORY_ENGINE_DELIVERED.md
INFORMATION_THEORY_ENGINE_READY.md
INFORMATION_THEORY_MATH_ENGINES_DEEP_ANALYSIS.md
INFRASTRUCTURE_CRITICAL_PATH_ANALYSIS_FRAMEWORK.md
INFRASTRUCTURE_KNOWLEDGE_BASE_SUMMARY.md
INTELLIGENCE_PIPELINE_END_TO_END_ANALYSIS.md
JOHHN_ATOMIC_LAYER_BLUEPRINT.md
JOHHN_E2E_COMPLETE_INTEGRATION_VALIDATED.md
JOHHN_E2E_IMPLEMENTATION_PLAN.md
JOHHN_GUARDIAN_FUSION_COMPLETE_PLAN.md
JOHHN_INFORMATION_THEORY_FLOW.md
JOHHN_INTEGRATION_BLUEPRINT.md
JOHHN_PRODUCTION_ACTIVATION.md
JOHHN_PRODUCTION_OUTCOMES.md
JOHN_QA_INSPECTOR_OPERATIONAL_ANALYSIS.md
LFG_ALL_SYSTEMS_OPERATIONAL.md
LIVESTREAM_CONTENT_STRATEGY_MON_TUE.md
LIVESTREAM_CONTENT_STRATEGY_MON_TUE.pdf
LIVESTREAM_DEEP_CODEBASE_ANALYSIS.md
LIVESTREAM_QUICK_REFERENCE.md
LIVESTREAM_QUICK_REFERENCE_MON_TUE.md
LIVESTREAM_QUICK_REFERENCE_MON_TUE.pdf
LIVESTREAM_TITLE_DESCRIPTION.md
LIVE_DEMO_QUICK_REFERENCE.md
LIVE_EVENT_TITLE_DESCRIPTION.md
LOCAL_AI_ASSISTANT_COMPLETE_LIVE_ANALYSIS.md
MASTER_EMERGENT_OS_STREAM.md
MCP_SERVERS_DEEP_ANALYSIS.md
META_GUARDIAN_CONVERGENCE_ANALYSIS.md
META_ORCHESTRATOR_ROCK_OUT_PLAN.md
MICHAELS_BLACK_PALETTE_OPERATIONALIZED.md
MICHAEL_DEPLOYMENT_ACTION_PLAN.md
MICHAEL_DESIGN_SYSTEM_SEARCH.md
NEUROMORPHIC_ARCHITECTURE_ANALYSIS.md
NEWSLETTER_DETECTION_EXPANSION.md
NEXT_LEVEL_EMERGENCE_CONVERGENCE.md
NEXT_STEPS.md
NEXT_STEPS_EXECUTED.md
OBSERVER_CONTEXT_EPISTEMIC_CERTAINTY.md
ONE_KERNEL_INTEGRATION_PLAN_PHASE0.md
ONE_ORGANISM_FUSION_PROTOCOL.md
OPTIMAL_FOLDER_HIERARCHY.md
OPTIMAL_SIMPLEST_PATH.md
OPTION_A_COMPLETE_IN_BROWSER.md
ORGANIC_UNIFICATION_OPPORTUNITIES.md
ORGANISM_LOCKED_IN.md
ORGANIZATION_EXECUTION_COMPLETE.md
ORGANIZATION_EXECUTION_STATUS.md
PLAYWRIGHT_AUTOMATION_READY.md
PLAYWRIGHT_CHALLENGE_FIXED.md
POCKETPATTERN_RESILIENCE_ANALYSIS.md
PRE_LAUNCH_SUMMARY.md
RADICAL_TRANSPARENCY_IMPLEMENTATION.md
README.md
RECURSIVE_ARCHITECTURE_CONVERGENCE_ANALYSIS.md
RECURSIVE_FORENSIC_CONVERGENCE_ANALYSIS.md
SHE_IS_ALIVE.md
SIMPLIFY_TO_AMPLIFY_ROADMAP.md
SINGULARITY_ACHIEVED.md
START_DEV_SERVER.md
STATE_AWARE_MASTER_CONTEXT.md
STRATEGIC_EEAaO_CRITICAL_PATH_INTEGRATION.md
SYNTHESIS_COMPLETE_EXCELLENCE.md
SYNTHESIS_COMPLETE_SUMMARY.md
SYSTEM_KNOWS_API_KEYS_ALWAYS.md
TERMINAL_TROUBLESHOOTING.md
THE_UNIFYING_PRINCIPLE.md
THREE_MAXIMUM_POWER_APPLICATIONS.md
TLDR_CONVERGENCE_ANALYSIS.md
TLDR_CONVERGENCE_INTEGRATED.md
TRANSCENDENT_AUTOMATION_CAPABILITIES.md
TRIADIC_UNITY_PROTOCOL.md
TROUBLESHOOTING.md
TRUICE_FUNNEL_ACTUAL_GAPS_ANALYSIS.md
TRUICE_LAUNCH_NOW.md
ULTIMATE_CONVERGENCE_EPISTEMIC_CERTAINTY.md
USER_JOURNEY_QA.md
V0_ETERNAL_FIX_SUMMARY.md
V0_PROJECT_COMPLETION_PROMPT.md
V0_PROJECT_CONTEXT.md
V0_PROJECT_DRIFT_ANALYSIS.md
VALIDATION_STATE_ANALYSIS.md
VALIDATION_SUMMARY.md
VALUABLE_ASSETS_QUICK_REFERENCE.md
VERMILLION_COLOR_FIX.md
VIRTUAL_ENVIRONMENT_DEEP_ANALYSIS.md
VISUAL_NEXT_STEPS.md
WEBINAR_JOHN_CERTIFICATION_OUTPUT.txt
WEBINAR_UNIFIED_ONE_VALIDATION.json
WHAT_ELSE_EMERGES.md
WHAT_INVITES_EMERGENCE_WHO_IDENTIFIES_CONVERGENCE.md
WHAT_LONGS_FOR_EMERGENCE.md
WHAT_LONGS_FOR_EMERGENCE_CONVERGENCE_SYNTHESIS.md
WHAT_LONGS_FOR_EMERGENCE_CONVERGENCE_VALIDATED.md
WHAT_LONGS_FOR_SIMPLIFICATION_ACTIVATION_UNIFICATION_CONVERGENCE_EMERGENCE.md
WHAT_LONGS_TO_BE_OPERATIONALIZED.md
WHAT_THE_SYSTEM_LONGS_FOR.md
WHAT_WE_CAN_BUILD_NOW.md
WHAT_WE_CAN_DO_WITH_ALL_THIS_POWER.md
WHAT_YOU_CAN_DO_NOW.md
WORKSPACE_CHROME_EXTENSION_ALIGNMENT.md
WORLD_SHOWCASE_PREPARATION.md
ZERO_ALLISON_PROFILE_EXTRACTION.md
ZERO_ALRAX_AEYON_FORENSIC_FIX.md
ZERO_COMPLETE_FORENSIC_AGENT_PERSONALITY_ANALYSIS.md
ZERO_FORENSIC_ANALYSIS_GZ360_BRAVETTO.md
ZERO_JOHN_SECURITY_AUDIT_REPORT.json
ZERO_JOHN_SECURITY_CERTIFICATION.md
_ABEBEATS_EXTRACTION_PLAN.md
_ABEBEATS_IDENTIFICATION_MAP.md
_BATCH_1_CORRECTED.md
_BATCH_1_DIFF_PREVIEW.md
_BATCH_1_DIFF_PREVIEW_ABEBEATS.md
_BATCH_1_VALIDATION_ABEBEATS.md
_BRAVETTO_ORBIT_BUILDER_ANALYSIS_REPORT.md
_BRAVETTO_ORBIT_BUILDER_PROMPT.md
_TRUICE_CANONICAL_VALIDATION.md
_TRUICE_HUMAN_PROVENANCE_MAP.md
_TRUICE_IMPORT_ANALYSIS.md
_cleanup_log.txt
access_all_repositories.sh
all_5_capabilities_validation.json
drift-dashboard-eternal.html
drift-visual-status.md
elegance_frictionless_validation.json
intentional_activation_verification.json
newsletters_config.json
package.json
parallel_concurrent_validation.json
pyrightconfig.json
repository_validator.py
test_aeyon_binding.py
test_aeyon_execution.py
test_aeyon_import.py
test_aeyon_integration.py
universal_repository_awareness.json
universal_repository_awareness.py
validate_aeyon_build.sh
validate_repository_access.sh
```