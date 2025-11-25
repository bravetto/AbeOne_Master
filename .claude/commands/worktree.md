# `/worktree` Command

Manage git worktrees for parallel feature development.

## Usage

```
/worktree [action] [branch] [path]
```

## Actions

- `create` - Create new worktree with branch
- `list` - List all worktrees
- `remove` - Remove worktree
- `switch` - Switch to worktree

## Examples

```
/worktree create feature/new-module ../feature-new-module
/worktree list
/worktree remove ../feature-new-module
```

