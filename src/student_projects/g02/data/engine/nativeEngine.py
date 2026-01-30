from engine.mathKernel import MathKernel


class NativePythonEngine(MathKernel):
    def find_stolen_nuts(self, data):
        stolen = 0
        for stash in data:
            if stash["amount"] < stash["expected_amount"]:
                stolen += 1
        return stolen
