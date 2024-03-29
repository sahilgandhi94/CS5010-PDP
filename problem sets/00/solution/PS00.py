''' solution class '''

from graph import Graph


class PS00:

    # The examples refer to
    #
    #     foo
    #     circularModules
    #     modules1
    #     modules2
    #     list(...)
    #
    # These are public static members of the ModuleExamples class
    # defined in moduleExamples.java

    # isCircular : ListOfModule -> Boolean
    # GIVEN: a list of module descriptions
    # WHERE: no two descriptions are for the same module name
    # RETURNS: true if and only if one or more of the modules
    #     depends upon itself
    # EXAMPLES:
    #
    #     isCircular (list())  =>  false
    #
    #     isCircular (modules1)  =>  false
    #
    #     isCircular (circularModules)  =>  true

    def isCircular(self, modules):
        return Graph.makegraph(modules).iscyclic()

    # bestMode : String ListOfModule -> String
    # GIVEN: a module name M and a list of module descriptions
    # WHERE: no two descriptions are for the same module name,
    #     M is among the modules described,
    #     and none of the described modules depend upon themselves
    # RETURNS: the name of a mode (LP64, ILP64, LP32, or ILP32)
    #     that, when used to compile all of the modules that need to be
    #     compiled before module M can be used, would result in
    #     compiling the fewest modules
    # NOTE: this function may have more than one correct result
    # EXAMPLES:
    #
    #     bestMode ("Main", modules1)  =>  "LP64"
    #
    #     bestMode ("Main", modules2)  =>  "ILP32"

    def bestMode (self, m, modules):
        # Your code goes here.
        return self._plan(m, modules)[1]

    # bestPlan : String ListOfModule -> ListOfString
    # GIVEN: a module name M and a list of module descriptions
    # WHERE: no two descriptions are for the same module name,
    #     M is among the modules described,
    #     and none of the described modules depend upon themselves
    # RETURNS: a list of names for the modules that need to be compiled
    #     using the best mode, in the order they should be compiled,
    #     before module M can be used
    # NOTE: this function may have more than one correct result
    # EXAMPLE:
    #
    # bestPlan ("Main", modules2)  =>  list ("List", "AList", "Main")

    def bestPlan (self, m, modules):
        # Your code goes here.
        return [mod.moduleName for mod in self._plan(m, modules)[0]]

    # Your help methods go here.

    def _plan(self, name, modules):
        ''' helper method for both bestPlan and bestMode '''
        grph = Graph.makegraph(modules)
        order = grph.order(module=name)
        tocompile = list()  # array of modules (in order) that needs to be compiled
        nocompile = list()  # array of modules (in order) that need not be compiled
        bestmode = None

        for module in order:
            if self._needscompilation(module, grph):
                # all modules starting from this module inside the order list needs to be compiled
                tocompile = order[order.index(module):]
                break
            else:
                nocompile.append(module)
        if nocompile:
            bestmode = nocompile[-1].compilationMode
        else:
            bestmode = tocompile[0].compilationMode

        return tocompile, bestmode
                

    def _needscompilation(self, module, grph):
        ''' checks for assertions such as (not in order)
            1. compilation time is after modified time or compilation time is -1
            2. compilation mode of all dependencies is same as its own
            3. compilation time is > all compilation time of its dependencies
        '''
        if module.compilationTime == -1 or module.compilationTime < module.modificationTime:
            return True
        for mod in grph.adj[module]:
            if mod.compilationTime > module.compilationTime:
                return True
            elif mod.compilationMode != module.compilationMode:
                return True

        return False
