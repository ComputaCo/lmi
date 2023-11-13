# I should move this to another repo and just import export it here


@component
def terminal():
    get_text, set_text, append_text = use_state("", append=True)

    get_subprocess, set_subprocess = use_state(
        lambda: subprocess.Popen(
            ["bash"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
    )

    @input(">>> ")
    def input(text):
        # write input to terminal
        append_text(f">>> {text}\n")
        # write input to subprocess
        proc = get_subprocess()
        proc.stdin.write(text.encode("utf-8"))
        # read output from subprocess
        append_text(proc.stdout.read().decode("utf-8"))

    return [
        get_text(),
        input,
    ]
