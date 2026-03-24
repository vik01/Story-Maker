# StoryMaker - Run wild with your ideas!

**Author:** Vikram Bhatt
**Version:** 1.0.0

---

## Description

The StoryMaker project is about using AI to build out short stories of different types ranging from fantasy to sci-fi to even more! I use OpenRouter to query the Arcee AI free model that is excellent at creative writing, story-telling, and much more! Additionally, the project is Object Oriented and uses classes to build out the story. It is a work in progress and there are many things I still want to add.

---

## Getting Started

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency and virtual environment management. **Python 3.12 or higher is required.**

### 1. Install uv

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or via pip (any platform):
```bash
pip install uv
```

### 2. Create the virtual environment and install dependencies

```bash
uv sync
```

This reads `pyproject.toml`, creates a `.venv` folder, and installs all required packages automatically.

### 3. Set up your API key

Create a `.env` file in the project root and add your OpenRouter API key:

```
OPENROUTER_API=your_api_key_here
```

### 4. Run the project

**Script (CLI):**
```bash
uv run main.py --files <story_folder> <story_file> <history_folder> <history_file>
```

**Streamlit app:**
```bash
uv run streamlit run app.py
```

---

## Assignment Points Covered

---

### 1. Classes

**Location:** `StoryMaker.py` lines 8–22 · `StoryHelper.py` lines 15–19

Two classes are defined: `StoryMaker` is the core AI generation class with a full class-level docstring listing its attributes. `StoryHelper` extends it and is defined in its own file.

![classes1](project_images/classes1.jpg)

![classes1](project_images/classes2.jpg)

---

### 2. Instances

**Location:** `main.py` lines 93–96 · `app.py` lines 18–21

`StoryMaker()` is instantiated inside `main()` based on user input — either with a custom system prompt or with the default. In `app.py`, `StoryHelper()` is instantiated inside a cached factory function.

![instances1](project_images/instances1.jpg)

![instances2](project_images/instances2.jpg)

---

### 3. Class Attributes

**Location:** `StoryMaker.py` lines 24–35

Five class-level attributes are defined directly on the `StoryMaker` class body (not inside `__init__`): `url`, `main_model`, `__fallback_models`, `basic_prompt`, and `init_sys_prompt`. These are shared across all instances.

![class_attributes1](project_images/class_attributes1.jpg)

---

### 4. Instance Attributes

**Location:** `StoryMaker.py` lines 49–53 · `StoryHelper.py` lines 18–19

`StoryMaker.__init__` sets four instance attributes: `self.temp`, `self.max_tokens`, `self.stream_result`, and `self.__preserve_convo`. `StoryHelper.__init__` sets `self.__story_path` and `self.__image_path` as `Path` objects unique to each instance.

![instance_attributes1](project_images/instance_attributes1.jpg)

![instance_attributes2](project_images/classes2.jpg)

---

### 5. Mutable / Immutable Attributes

**Location:** `StoryMaker.py` lines 25–35 (class) · lines 49–53 (instance)

Class attributes `url`, `main_model`, and `basic_prompt` are strings — **immutable** in Python. Instance attribute `self.__preserve_convo` is a list — **mutable**, and is explicitly modified throughout the class via `.append()` and `.clear()`.

![mutable_immutable2](project_images/mutable_immutable.jpg)

---

### 6. Hashable Objects

**Location:** `StoryHelper.py` lines 7–13 · `app.py` lines 62–67 · `app.py` line 205

`StoryRecord` is a `namedtuple` — immutable and therefore hashable. This allows it to be used directly as a **dictionary key** in `st.session_state.generated_stories`, which maps each story archetype to its generated text. Plain dicts or lists cannot be used as dict keys.

![hashable1](project_images/hashable1.jpg)

![hashable2](project_images/hashable2.jpg)

![hashable3](project_images/hashable3.jpg)

---

### 7. Magic Methods

**Location:** `StoryMaker.py` lines 37–66 · lines 281–302

Four dunder methods are implemented in `StoryMaker`:
- `__init__` (lines 37–66): sets up instance state and conversation history
- `__del__` (lines 281–286): safety-net cleanup when object is garbage collected
- `__enter__` (lines 289–291): enables use as a `with` statement, returns `self`
- `__exit__` (lines 294–302): guaranteed cleanup when the `with` block exits

![magic_methods1](project_images/magic_methods1.jpg)

---

### 8. Docstrings

**Location:** `StoryMaker.py` lines 9–22 · lines 38–47 · `StoryHelper.py` lines 65–76

Google-style docstrings are used throughout. The class has an `Attributes` section. Methods have `Args`, `Returns`, and `Yields` sections where applicable. One-liners are used for simple methods (e.g., `close()`).

![docstrings1](project_images/docstrings1.jpg)

---

### 9. Inheritance

**Location:** `StoryHelper.py` line 15 · lines 171–174

`StoryHelper` inherits from `StoryMaker` using `class StoryHelper(StoryMaker)`. `super().__init__(system_prompt)` is called inside `generate_story()` rather than in `__init__` — this intentionally defers parent initialisation until a system prompt is available at generation time.

`class StoryHelper(StoryMaker):`

`super().__init__(system_prompt)`

---

### 10. Composition

**Location:** `StoryMaker.py` lines 69–71 · lines 154–155

`StoryMaker` uses **composition** by holding an `OpenAI` client object (`self.client`) as an instance attribute. The client is created lazily via `__create_client()` and is only instantiated when `generate()` or `stream_generate()` is first called.

```python
    def __create_client(self):
        """Creates and assigns the OpenAI HTTP client. Called lazily by generate()."""
        self.client = OpenAI(base_url=self.url, api_key=open_ai_key)
```

---

### 11. \*args

**Location:** `StoryHelper.py` line 150 · lines 178–185

`generate_story()` accepts `*args` to receive a variable number of story detail strings (protagonist, description, setting, etc.) from the Streamlit app. The args are then iterated with `zip(labels, args)` to assemble a structured prompt.

```python
def generate_story(self, system_prompt: str, *args):
    """
    Initialize StoryMaker with a system prompt and generate a story.

    Calling super().__init__() here (rather than in StoryHelper.__init__)
    lets us inject the user-selected system prompt at generation time.
    Each call starts a fresh StoryMaker conversation, so successive calls
    are independent of one another.

    Args:
        system_prompt (str): The full system prompt text to pass to
            StoryMaker (e.g. the "system_prompt" field from a prompt dict).
        *args: Story detail strings passed in from the Streamlit app,
            expected in this order:
                protagonist, description, setting, plot,
                conflict, theme, point_of_view
            These are assembled into a structured prompt for the model.

    Returns:
        str: The generated story text from StoryMaker.
    """
    # Re-initialize StoryMaker fresh with the chosen system prompt.
    # stream_generate() handles streaming internally, so turn_on_streaming()
    # is not needed here.
    super().__init__(system_prompt)

    # Assemble the story fields into a structured prompt for the model.
    # The labels match the order the Streamlit app passes the args.
    labels = [
        "Protagonist", "Description", "Setting",
        "Plot", "Conflict", "Theme", "Point of View"
    ]
    prompt_lines = ["Write a story with the following details:"]
    for label, value in zip(labels, args):
        prompt_lines.append(f"- {label}: {value}")
    prompt = "\n".join(prompt_lines)

    # yield from turns generate_story() into a generator, so the caller
    # (e.g. st.write_stream) receives chunks as they arrive from the model.
    yield from self.stream_generate(prompt)
```

---

### 12. \*\*kwargs

**Location:** `StoryMaker.py` lines 191–219 · `main.py` lines 39–40

`StoryMaker.update()` accepts `**kwargs` and iterates over them to build an update instruction for the model. `update_storyMaker()` in `main.py` passes `**updates` through to `story.update()`.

---

### 13. Default Arguments

**Location:** `StoryMaker.py` lines 37, 164, 223

Three methods demonstrate default argument values:
- `__init__(self, system_prompt:str="")` — defaults to the built-in system prompt
- `generate(self, prompt:str="")` — defaults to `basic_prompt`
- `get_convo_history(self, pretty:bool=False)` — defaults to raw list output

---

### 14. Positional Arguments

**Location:** `main.py` lines 36–37 · lines 131–132

`generate_storyMaker(story, prompt)` defines and calls arguments positionally. `story_maker` and `prompt` are passed in order without keyword labels at the call site on line 132.

```python
def generate_storyMaker(story:StoryMaker, prompt:str=""):
    return story.generate(prompt)
```

---

### 15. Keyword Arguments

**Location:** `main.py` lines 85–90 · line 137

`ask()` is called with all three parameters passed by keyword name (`qn=`, `err=`, `err_check_type=`), making the call site self-documenting. On line 137, `close_storyMaker` is called with `pretty=True` as a keyword argument.

```python
def ask(qn:str, err:str, err_check_type:str):
    ans = input(qn + "\n Answer:")
    while not check_correct(err_check_type, ans):
        print(err)
        ans = input(qn + "\n Answer:")
    return ans
```

---

### 16. Decorators

**Location:** `main.py` lines 28–44 · `StoryMaker.py` lines 305–308 · `app.py` lines 17–19, 28–31

Four decorator types are demonstrated:
- **Custom decorator** with `@functools.wraps` (`main.py` lines 28–34) — captures conversation history before closing
- **`@get_conversation_storyMaker`** applied to `close_storyMaker` (`main.py` lines 42–44)
- **`@classmethod`** on multiple utility methods (`StoryMaker.py` lines 305–308)
- **`@st.cache_resource`** and **`@st.cache_data`** in `app.py`

```python
def get_conversation_storyMaker(func):
    @functools.wraps(func)
    def wrapper(story:StoryMaker, pretty:bool=True):
        history = story.get_convo_history(pretty)
        func(story)
        return history
    return wrapper

@get_conversation_storyMaker
def close_storyMaker(story:StoryMaker):
    story.close()
```

---

### 17. Generators

**Location:** `StoryMaker.py` lines 102–136 · lines 139–161 · `StoryHelper.py` line 189

`__stream_chat()` uses `yield` to send each text chunk from the API to the caller as it arrives, then appends the complete response to history after the loop. `stream_generate()` uses `yield from` to delegate to `__stream_chat()`. `generate_story()` in `StoryHelper` also uses `yield from` to chain the whole pipeline, enabling `st.write_stream()` to consume it directly.

```python
def __stream_chat(self):
        """
        Generator version of __chat() for streaming output.

        Makes the same API call as __chat() but always streams, yielding each
        text chunk as it arrives instead of printing it. After all chunks have
        been yielded, the complete response is appended to conversation history
        exactly like __chat() does, keeping the history consistent.

        Yields:
            str: Individual text chunks from the model as they arrive.
        """
        response = self.client.chat.completions.create(
            model=self.main_model,
            messages=self.__preserve_convo,
            extra_body={
                "models": self.__fallback_models
            },
            max_tokens=self.max_tokens,
            stream=True,                 # always stream in this path
            temperature=self.temp
        )

        complete_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                complete_response += content
                yield content            # send chunk to the caller

        # Append the full assembled response to history once streaming is done
        self.__preserve_convo.append({
            "role": "assistant",
            "content": complete_response,
        })


def stream_generate(self, prompt: str = ""):
    """
    Generator version of generate() that yields text chunks for streaming.

    Intended for use with Streamlit's st.write_stream() or any other caller
    that consumes a generator. Creates the HTTP client on first call if it
    does not already exist.

    Args:
        prompt (str): The story prompt to send to the model. If empty, the
            default basic_prompt is used.

    Yields:
        str: Individual text chunks from the model as they arrive.
    """
    if not hasattr(self, 'client'):
        self.__create_client()

    message = {"role": "user", "content": prompt if prompt else self.basic_prompt}
    self.__preserve_convo.append(message)

    # Delegate to __stream_chat() which handles the streaming loop
    yield from self.__stream_chat()
```

---

### 18. Scripts

**Location:** `main.py` lines 7–8, 22–26, 164–165

`main.py` is structured as a proper Python script: `argparse` is configured at module level, the entry point is guarded with `if __name__ == "__main__":`, and `main()` contains all runtime logic.

---

### 19. Paths

**Location:** `main.py` lines 5, 11–12, 14–18, 140–147 · `StoryHelper.py` lines 5, 18–19, 24, 43, 115

`pathlib.Path` is used in both scripts. In `main.py`, paths are built with the `/` operator, checked with `.exists()`, and files are opened with `.open("a")`. In `StoryHelper.py`, all JSON and image paths are composed the same way, replacing all f-string path concatenation.

`from pathlib import Path`

```python
# story file
with story_path.open("a") as f:
    f.write(initial_story)
    f.write("")

# history file
with history_path.open("a") as f:
    f.write(conversation)
    f.write("")
```

```python
def ensure_files(files):
    story_path   = Path(files[0]) / files[1]
    history_path = Path(files[2]) / files[3]

    if not story_path.exists():
        raise FileNotFoundError("Story file not found. Please check the path or create the story.")

    if not history_path.exists():
        raise FileNotFoundError("History file not found. Please check the path or create the story.")

    return story_path, history_path
```

---

### 20. Collections

**Location:** `StoryHelper.py` lines 2, 7–13 · lines 26–38

`namedtuple` from the `collections` module is used to define `StoryRecord` — a lightweight, immutable record for a story archetype. `__load_helpers()` converts each raw JSON dict into a `StoryRecord` instance using a list comprehension, flattening the nested `characters` sub-dict.

![collections1](project_images/collections1.jpg)

---

### 21. Iterables

**Location:** `StoryHelper.py` lines 183–184 · `StoryMaker.py` lines 241–244 · `app.py` lines 50, 245–255

Iterables are used throughout: `zip(labels, args)` pairs field labels with values in `generate_story()`; a `for` loop iterates over `__preserve_convo` in `get_convo_history()`; a dict comprehension builds `story_lookup` in `app.py`; and `dict.items()` is iterated in the Created Stories tab.

![iterables1](project_images/iterables1.jpg)

![iterables2](project_images/iterables2.jpg)

---

### 22. Pass by Reference vs Copy

**Location:** `StoryMaker.py` lines 236–237

`get_convo_history(pretty=False)` returns `list(self.__preserve_convo)` — a **shallow copy** — rather than the list itself. Returning the list directly would pass a reference to the internal state, allowing the caller to corrupt conversation history with appends or removals.

![pass_by_reference1](project_images/shallow_copy1.jpg)

---

### 23. Deep / Shallow Copy

**Location:** `StoryMaker.py` lines 236–237

`list(self.__preserve_convo)` creates a **shallow copy** — a new list object, but the dict elements inside still point to the same objects as the original. This is sufficient here since callers receiving the history are not expected to mutate the message dicts. A `copy.deepcopy()` would fully isolate the nested dicts but is not needed for this use case.

![shallow_copy1](project_images/shallow_copy1.jpg)

---

### 24. Menus

**Location:** `main.py` lines 46–67 · lines 83–105

`check_correct(question, answer)` validates input differently depending on the question type. `ask(qn, err, err_check_type)` wraps `input()` in a `while` loop that re-prompts until a valid answer is given. The `main()` function presents two numbered menus using these helpers.

![menus1](project_images/while_loops2.jpg)

---

### 25. argparse

**Location:** `main.py` lines 3, 7–8, 22–26

`argparse.ArgumentParser` is used to accept `--files` from the command line. The argument takes exactly 4 values (`nargs=4`) — story folder, story filename, history folder, history filename. `parse_args()` is called at module level so arguments are available throughout the script.

![argparse1](project_images/argparse1.jpg)

---

### 26. APIs

**Location:** `StoryMaker.py` lines 1–6, 69–71, 83–99, 114–136

The OpenRouter API is called via the OpenAI-compatible SDK. The client is initialised lazily with a base URL and API key. Both `__chat()` (non-streaming) and `__stream_chat()` (streaming) send the full conversation history to the model and handle the response, including fallback models via `extra_body`.

`from openai import OpenAI`

![apis1](project_images/apis.jpg)

---

### 27. .env

**Location:** `StoryMaker.py` lines 1, 5–6

`python-dotenv`'s `dotenv_values(".env")` loads the `.env` file at module level and extracts the `OPENROUTER_API` key. This keeps the API key out of source code and out of version control.

![dotenv1](project_images/dotenv1.jpg)

---

### 28. README.md

**Location:** `README.md` lines 1–144

The README covers: project title and description, a Features section with three screenshots, full Getting Started instructions for macOS/Linux/Windows using `uv`, file structure with annotations, a dependencies table, and a Next Steps checklist.

![readme1](project_images/README.jpg)

---

### 29. pyproject.toml

**Location:** `pyproject.toml` lines 1–17

All project metadata and dependencies are declared in `pyproject.toml` using the `uv` standard. Every package that is directly imported (`openai`, `python-dotenv`, `streamlit`, `pillow`, `pandas`) is listed as a direct dependency with a minimum version constraint.

> VIKRAM - NEED TO ADD IMAGE. Python file pyproject.toml lines 1-17

![pyproject1](project_images/pyproject1.jpg)

---

### 30. Object Scope

**Location:** `StoryMaker.py` lines 24–35 (class scope) · lines 49–53 (instance scope) · `StoryHelper.py` lines 7–13 (module scope)

Three scopes are demonstrated: `StoryRecord` is defined at **module scope** in `StoryHelper.py`; `url`, `main_model`, etc. are **class-scope** attributes shared by all instances; `self.temp`, `self.__preserve_convo`, etc. are **instance-scope** attributes unique per object. Private name mangling (`__preserve_convo`, `__story_path`) is used to restrict access.

![object_scope1](project_images/object_scope1.jpg)

![object_scope2](project_images/mutable_immutable.jpg)

---

### 31. For Loops

**Location:** `StoryMaker.py` lines 213–214, 241–244 · `StoryHelper.py` lines 183–184 · `app.py` lines 163–164, 245–255

For loops are used throughout: iterating over `kwargs.items()` to build update messages, iterating over `__preserve_convo` to format history, `zip(labels, args)` to assemble prompts, and iterating over `generated_stories.items()` to render the Created Stories tab.

![for_loops1](project_images/for_loops1.jpg)

![for_loops2](project_images/for_loops2.jpg)

---

### 32. While Loops

**Location:** `main.py` lines 64–67 · lines 83–161

Two while loops are present: `ask()` uses `while not check_correct(...)` to re-prompt the user until their input is valid. `main()` uses `while condition_num != 1` as the main application loop — set `condition_num = 1` to exit, otherwise the loop continues for another story generation cycle.

![while_loops1](project_images/while_loops1.jpg)

![while_loops2](project_images/while_loops2.jpg)
