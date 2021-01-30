import ptm_functions as ptm

# Instead of using if-else, this handy dict
# does the same thing, and it's more elegant
func_equiv = {
    "new": ptm.new_task,
    "edit": ptm.edit_task,
    "del": ptm.del_task,
    "done": ptm.mark_done
}

ptm.display()
while True:
    cmd = ptm.valid_command()
    try:
        func_equiv[cmd[0]](cmd)
    except TypeError:
        print("Invalid number of arguments.")
        ptm.sleep()
    ptm.cls()
    ptm.display()
