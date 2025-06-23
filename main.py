import tkinter as tk
from tkinter import simpledialog

# Simulated Git File
class GitFile:
    def __init__(self, name):
        self.name = name
        self.modified = False
        self.staged = False
        self.committed = False
        self.content = ""
        self.last_commit_content = ""

# Guided Tutorial
class GuidedTutorial:
    def __init__(self):
        self.steps = [
            ("git init", "📘 Step 1: Start your Git journey with `git init`."),
            ("New", "📘 Step 2: Create a new file to start working on."),
            ("Save", "📘 Step 3: Save changes to the file."),
            ("git add", "📘 Step 4: Stage your changes using `git add`."),
            ("git commit", "📘 Step 5: Commit the staged changes."),
            ("git status", "📘 Step 6: Check which files are staged or modified."),
            ("git log", "📘 Step 7: View your commit history."),
            ("ls-files", "📘 Step 8: See files tracked in the current branch."),
            ("git branch", "📘 Step 9: Explore branches using `git branch`."),
            ("git checkout", "📘 Step 10: Switch or create branches."),
            ("git merge", "📘 Step 11: Merge another branch into this one."),
            ("git remote add", "📘 Step 12: Simulate adding a remote."),
            ("git push", "📘 Step 13: Simulate pushing to remote."),
            ("git pull", "📘 Step 14: Simulate pulling from remote.")
        ]
        self.current_step = 0

    def get_instruction(self):
        if self.current_step < len(self.steps):
            return self.steps[self.current_step][1]
        return "🎉 Tutorial complete!"

    def advance_step(self, command):
        if self.current_step < len(self.steps):
            expected = self.steps[self.current_step][0]
            if command == expected:
                self.current_step += 1
                return True
        return False

# Main App
class GitSimulator:
    def __init__(self, master):
        self.master = master
        master.title("🌙 Git Learning Playground")
        master.configure(bg="#1e1e2f")
        self.tutorial = GuidedTutorial()

        # Git state
        self.repo_initialized = False
        self.current_branch = "main"
        self.files = {}  # currently loaded files
        self.branch_files = {"main": {}}  # branch_name: {filename: content}
        self.branches = {"main": []}  # branch_name: commit list
        self.commit_history = []
        self.remote_connected = False
        self.current_file = None

        # Layout
        self.top_frame = tk.Frame(master, bg="#1e1e2f")
        self.top_frame.pack(side=tk.TOP, fill="both", expand=True)
        self.bottom_frame = tk.Frame(master, bg="#1e1e2f")
        self.bottom_frame.pack(side=tk.BOTTOM, fill="x")

        self.main_frame = tk.Frame(self.top_frame, bg="#1e1e2f", width=300)
        self.main_frame.pack(side=tk.LEFT, fill="y")

        self.editor_frame = tk.Frame(self.top_frame, bg="#282a36")
        self.editor_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)

        self.tutorial_frame = tk.Frame(self.top_frame, width=250, bg="#202030")
        self.tutorial_frame.pack(side=tk.RIGHT, fill="y")

        tk.Label(self.main_frame, text="Git Playground 🧠", font=("Segoe UI", 16, "bold"),
                 bg="#1e1e2f", fg="#f8f8f2").pack(pady=10)

        # Button sections
        self.setup_section("📁 File Actions", [
            ("New", self.new_file, "Create new file"),
            ("Open", self.open_file_dialog, "Open file in editor"),
            ("Save", self.save_file, "Save changes to file"),
            ("Reset", self.reset_file, "Reset file to last commit")
        ])
        self.setup_section("🔧 Basic Git Actions", [
            ("git init", self.git_init, "Initialize repo"),
            ("git add", self.git_add, "Stage changes"),
            ("git commit", self.git_commit, "Commit staged changes")
        ])
        self.setup_section("🔍 More Git Actions", [
            ("git status", self.git_status, "Show status"),
            ("git log", self.git_log, "Commit log"),
            ("ls-files", self.git_ls_files, "List tracked files")
        ])
        self.setup_section("🌿 Branching", [
            ("git branch", self.git_branch, "List branches"),
            ("git checkout", self.git_checkout, "Switch/create branch"),
            ("git merge", self.git_merge, "Merge a branch")
        ])
        self.setup_section("☁️ Remote", [
            ("git remote add", self.git_remote_add, "Simulate remote"),
            ("git push", self.git_push, "Push to remote"),
            ("git pull", self.git_pull, "Pull from remote")
        ])

        # Text editor
        tk.Label(self.editor_frame, text="📝 Simulated File Content", font=("Segoe UI", 12, "bold"),
                 bg="#282a36", fg="#f8f8f2").pack(anchor="w", padx=10, pady=5)
        self.text_editor = tk.Text(self.editor_frame, font=("Consolas", 11), bg="#1e1e2f", fg="#f8f8f2")
        self.text_editor.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.text_editor.config(state=tk.DISABLED)
        self.text_editor.bind("<<Modified>>", self.on_text_modified)

        # Tutorial
        tk.Label(self.tutorial_frame, text="📘 Guided Tutorial", font=("Segoe UI", 12, "bold"),
                 bg="#202030", fg="#8be9fd").pack(padx=10, pady=(10, 5), anchor="w")
        self.tutorial_text = tk.Text(self.tutorial_frame, width=35, height=30, wrap="word",
                                     font=("Segoe UI", 9), bg="#282a36", fg="#f8f8f2", bd=0)
        self.tutorial_text.pack(padx=10, pady=5)
        self.update_tutorial()

        # Console output
        self.text_output = tk.Text(self.bottom_frame, height=12, wrap="word", font=("Consolas", 10),
                                   bg="#282a36", fg="#f8f8f2", insertbackground="#f8f8f2")
        self.text_output.pack(fill="x", padx=10, pady=10)

    def setup_section(self, title, buttons):
        frame = tk.Frame(self.main_frame, bg="#1e1e2f")
        tk.Label(frame, text=title, font=("Segoe UI", 12, "bold"),
                 bg="#1e1e2f", fg="#f8f8f2").pack(anchor="w", padx=10, pady=(5, 0))
        btn_frame = tk.Frame(frame, bg="#1e1e2f")
        btn_frame.pack(padx=10, pady=5)
        for i, (text, func, tooltip) in enumerate(buttons):
            btn = tk.Button(btn_frame, text=text, width=14, command=lambda t=text, f=func: self.wrap_action(t, f),
                            bg="#44475a", fg="#f8f8f2", activebackground="#6272a4")
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
        frame.pack(fill="x", pady=5)

    def wrap_action(self, name, func):
        func()
        if self.tutorial.advance_step(name):
            self.update_tutorial()

    def update_tutorial(self):
        self.tutorial_text.config(state=tk.NORMAL)
        self.tutorial_text.delete("1.0", tk.END)
        self.tutorial_text.insert(tk.END, self.tutorial.get_instruction())
        self.tutorial_text.config(state=tk.DISABLED)

    def print_output(self, msg):
        self.text_output.insert(tk.END, f"👉 {msg}\n")
        self.text_output.see(tk.END)

    def on_text_modified(self, event=None):
        if self.current_file:
            if self.text_editor.edit_modified():
                content = self.text_editor.get("1.0", tk.END).rstrip("\n")
                self.files[self.current_file].content = content
                self.files[self.current_file].modified = True
                self.text_editor.edit_modified(0)

    # -------- FILE ACTIONS --------
    def new_file(self):
        if not self.repo_initialized:
            self.print_output("Repo not initialized.")
            return
        name = simpledialog.askstring("New File", "Enter new filename:")
        if name and name not in self.files:
            self.files[name] = GitFile(name)
            self.print_output(f"📄 Created '{name}'")
            self.open_file(name)

    def open_file_dialog(self):
        name = simpledialog.askstring("Open File", "Enter filename to open:")
        if name in self.files:
            self.open_file(name)
        else:
            self.print_output(f"'{name}' not found.")

    def open_file(self, name):
        self.current_file = name
        f = self.files[name]
        self.text_editor.config(state=tk.NORMAL)
        self.text_editor.delete("1.0", tk.END)
        self.text_editor.insert(tk.END, f.content)
        self.text_editor.edit_modified(0)
        self.print_output(f"Opened '{name}'")

    def save_file(self):
        if self.current_file:
            content = self.text_editor.get("1.0", tk.END).rstrip("\n")
            f = self.files[self.current_file]
            f.content = content
            f.modified = True
            self.print_output(f"💾 Saved '{self.current_file}'")
        else:
            self.print_output("No file is currently open.")

    def reset_file(self):
        if self.current_file:
            f = self.files[self.current_file]
            f.content = f.last_commit_content
            f.modified = f.staged = False
            self.open_file(self.current_file)
            self.print_output(f"🔁 Reset '{self.current_file}' to last commit.")
        else:
            self.print_output("No file is currently open.")

    # -------- GIT COMMANDS --------
    def git_init(self):
        self.repo_initialized = True
        self.print_output("🟢 Git repository initialized.")

    def git_add(self):
        added = False
        for f in self.files.values():
            if f.modified:
                f.staged = True
                added = True
        self.print_output("✅ Changes staged." if added else "Nothing to add.")

    def git_commit(self):
        staged = [f for f in self.files.values() if f.staged]
        if not staged:
            self.print_output("Nothing to commit.")
            return
        msg = simpledialog.askstring("Commit", "Enter commit message:")
        if msg:
            for f in staged:
                f.modified = f.staged = False
                f.committed = True
                f.last_commit_content = f.content
                self.branch_files[self.current_branch][f.name] = f.content
            self.commit_history.append(msg)
            self.branches[self.current_branch].append(msg)
            self.print_output(f"📦 Committed: '{msg}'")

    def git_log(self):
        self.print_output("📜 Commit Log:")
        for msg in reversed(self.branches[self.current_branch]):
            self.print_output(f" - {msg}")

    def git_status(self):
        self.print_output("📊 Git Status:")
        for name, f in self.files.items():
            if f.staged:
                self.print_output(f"✅ Staged: {name}")
            elif f.modified:
                self.print_output(f"✏️ Modified: {name}")
            elif not f.committed:
                self.print_output(f"📄 Untracked: {name}")

    def git_ls_files(self):
        self.print_output(f"📂 Files in branch '{self.current_branch}':")
        for name in self.branch_files.get(self.current_branch, {}):
            self.print_output(f" - {name}")

    def git_branch(self):
        for b in self.branches:
            tag = " (current)" if b == self.current_branch else ""
            self.print_output(f"🌿 {b}{tag}")

    def git_checkout(self):
        b = simpledialog.askstring("Checkout", "Enter branch name:")
        if b:
            if b not in self.branches:
                self.branches[b] = []
                self.branch_files[b] = {}
                self.print_output(f"🌱 Created new branch '{b}'")
            self.current_branch = b
            self.files.clear()
            for name, content in self.branch_files[b].items():
                f = GitFile(name)
                f.content = content
                f.last_commit_content = content
                f.committed = True
                self.files[name] = f
            self.print_output(f"🔀 Switched to branch '{b}'")

    def git_merge(self):
        b = simpledialog.askstring("Merge", "Enter branch to merge:")
        if b and b != self.current_branch and b in self.branch_files:
            for name, content in self.branch_files[b].items():
                self.files[name] = GitFile(name)
                self.files[name].content = content
                self.files[name].last_commit_content = content
                self.files[name].committed = True
                self.branch_files[self.current_branch][name] = content
            self.print_output(f"🔁 Merged '{b}' into '{self.current_branch}'")
        else:
            self.print_output("Invalid branch.")

    def git_remote_add(self):
        self.remote_connected = True
        self.print_output("🔗 Remote added.")

    def git_push(self):
        if self.remote_connected:
            self.print_output("🚀 Pushed to remote.")
        else:
            self.print_output("❌ No remote set.")

    def git_pull(self):
        if self.remote_connected:
            self.print_output("📥 Pulled from remote.")
        else:
            self.print_output("❌ No remote set.")

# Run it
if __name__ == "__main__":
    root = tk.Tk()
    app = GitSimulator(root)
    root.mainloop()
