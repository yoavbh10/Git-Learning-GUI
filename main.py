import tkinter as tk
from tkinter import simpledialog

class GitFile:
    def __init__(self, name):
        self.name = name
        self.modified = False
        self.staged = False
        self.committed = False

class GitSimulator:
    def __init__(self, master):
        self.master = master
        master.title("🌙 Git Learning Playground")

        # Dark mode colors
        self.bg_color = "#1e1e2f"
        self.fg_color = "#f8f8f2"
        self.btn_color = "#44475a"
        self.hover_color = "#6272a4"
        self.font = ("Segoe UI", 10)

        master.configure(bg=self.bg_color)

        # Git state
        self.repo_initialized = False
        self.files = {
            "main.py": GitFile("main.py"),
            "utils.py": GitFile("utils.py"),
            "README.md": GitFile("README.md")
        }
        self.commit_history = []
        self.current_branch = "main"
        self.branches = {"main": []}
        self.remote_connected = False

        # Title
        self.title = tk.Label(master, text="Welcome to Git Playground 🧠", font=("Segoe UI", 16, "bold"),
                              bg=self.bg_color, fg=self.fg_color)
        self.title.pack(pady=10)

        # Action sections
        self.setup_section("📁 File Actions", [
            ("Edit File", self.edit_file),
            ("Reset File", self.reset_file)
        ])

        self.setup_section("🔧 Basic Git Actions", [
            ("git init", self.git_init),
            ("git add", self.git_add),
            ("git status", self.git_status),
            ("git commit", self.git_commit),
            ("git log", self.git_log)
        ])

        self.setup_section("🌿 Branching", [
            ("git branch", self.git_branch),
            ("git checkout", self.git_checkout),
            ("git merge", self.git_merge)
        ])

        self.setup_section("☁️ Remote Actions", [
            ("git remote add", self.git_remote_add),
            ("git push", self.git_push),
            ("git pull", self.git_pull)
        ])

        # Output text box
        self.text_output = tk.Text(master, height=18, width=90, wrap="word", font=("Consolas", 10),
                                   bg="#282a36", fg=self.fg_color, insertbackground=self.fg_color)
        self.text_output.pack(pady=10)

    def setup_section(self, title, buttons):
        frame = tk.Frame(self.master, bg=self.bg_color)
        label = tk.Label(frame, text=title, font=("Segoe UI", 12, "bold"), bg=self.bg_color, fg=self.fg_color)
        label.pack(anchor="w", padx=10, pady=(5, 0))

        btn_frame = tk.Frame(frame, bg=self.bg_color)
        btn_frame.pack(padx=10, pady=5)

        for i, (text, command) in enumerate(buttons):
            b = tk.Button(btn_frame, text=text, font=self.font,
                          bg=self.btn_color, fg=self.fg_color, width=14, command=command,
                          activebackground=self.hover_color, activeforeground=self.fg_color)
            b.grid(row=0, column=i, padx=5, pady=5)

        frame.pack(fill="x", pady=5)

    def print_output(self, message):
        self.text_output.insert(tk.END, "👉 " + message + "\n")
        self.text_output.see(tk.END)

    # File actions
    def edit_file(self):
        if not self.repo_initialized:
            self.print_output("Please initialize the repository first.")
            return
        file = simpledialog.askstring("Edit File", "Enter file name to modify:")
        if file in self.files:
            self.files[file].modified = True
            self.print_output(f"📝 You made changes to '{file}'.")
        else:
            self.print_output(f"'{file}' does not exist in the project.")

    def reset_file(self):
        file = simpledialog.askstring("Reset File", "Enter file name to reset:")
        if file in self.files:
            self.files[file].modified = False
            self.files[file].staged = False
            self.print_output(f"🔁 '{file}' has been reset to last committed state.")
        else:
            self.print_output(f"'{file}' not found.")

    # Git core actions
    def git_init(self):
        if not self.repo_initialized:
            self.repo_initialized = True
            self.print_output("🟢 Git repository initialized.")
        else:
            self.print_output("Repository already initialized.")

    def git_add(self):
        if not self.repo_initialized:
            self.print_output("You must run 'git init' first.")
            return
        added_any = False
        for f in self.files.values():
            if f.modified:
                f.staged = True
                added_any = True
        if added_any:
            self.print_output("✅ Changes staged for commit.")
        else:
            self.print_output("No modified files to stage.")

    def git_status(self):
        if not self.repo_initialized:
            self.print_output("Initialize the repository to see status.")
            return
        self.print_output("📊 Git Status:")
        for name, f in self.files.items():
            if f.staged:
                self.print_output(f"  ✅ Staged: {name}")
            elif f.modified:
                self.print_output(f"  ✏️ Modified (not staged): {name}")
            elif not f.committed:
                self.print_output(f"  📄 Untracked: {name}")
        if all(not (f.modified or f.staged) for f in self.files.values()):
            self.print_output("  Working directory clean.")

    def git_commit(self):
        if not self.repo_initialized:
            self.print_output("Please initialize the repository first.")
            return
        staged = [f for f in self.files.values() if f.staged]
        if not staged:
            self.print_output("Nothing to commit.")
            return
        msg = simpledialog.askstring("Commit Message", "Enter commit message:")
        if msg:
            for f in staged:
                f.modified = False
                f.staged = False
                f.committed = True
            entry = f"{msg} (branch: {self.current_branch})"
            self.commit_history.append(entry)
            self.branches[self.current_branch].append(entry)
            self.print_output(f"📦 Commit saved: '{msg}'")
        else:
            self.print_output("Commit cancelled.")

    def git_log(self):
        if not self.repo_initialized:
            self.print_output("Repo not initialized.")
            return
        log = self.branches.get(self.current_branch, [])
        if not log:
            self.print_output("No commits yet.")
        else:
            self.print_output("📜 Commit log:")
            for entry in reversed(log):
                self.print_output(f"  - {entry}")

    # Branching actions
    def git_branch(self):
        if not self.repo_initialized:
            self.print_output("Please initialize the repository.")
            return
        self.print_output("🌿 Branches:")
        for branch in self.branches:
            tag = " (current)" if branch == self.current_branch else ""
            self.print_output(f"  - {branch}{tag}")

    def git_checkout(self):
        if not self.repo_initialized:
            self.print_output("Initialize the repo first.")
            return
        branch = simpledialog.askstring("Checkout Branch", "Enter branch to switch to:")
        if not branch:
            self.print_output("Checkout cancelled.")
            return
        if branch not in self.branches:
            self.branches[branch] = []
            self.print_output(f"🌱 Created and switched to new branch '{branch}'.")
        else:
            self.print_output(f"🔁 Switched to existing branch '{branch}'.")
        self.current_branch = branch

    def git_merge(self):
        if not self.repo_initialized:
            self.print_output("Initialize a repo first.")
            return
        source = simpledialog.askstring("Merge", "Enter source branch to merge from:")
        if not source or source not in self.branches:
            self.print_output(f"Branch '{source}' does not exist.")
            return
        if source == self.current_branch:
            self.print_output("Cannot merge a branch into itself.")
            return
        self.branches[self.current_branch].extend(self.branches[source])
        self.print_output(f"🔀 Merged branch '{source}' into '{self.current_branch}'.")

    # Remote actions
    def git_remote_add(self):
        if not self.repo_initialized:
            self.print_output("Init the repo first.")
            return
        self.remote_connected = True
        self.print_output("🔗 Remote 'origin' added (simulated).")

    def git_push(self):
        if not self.remote_connected:
            self.print_output("No remote found. Use 'git remote add' first.")
            return
        self.print_output(f"🚀 Pushed branch '{self.current_branch}' to remote.")

    def git_pull(self):
        if not self.remote_connected:
            self.print_output("No remote to pull from.")
            return
        self.print_output(f"📥 Pulled latest changes into '{self.current_branch}'.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = GitSimulator(root)
    root.mainloop()
