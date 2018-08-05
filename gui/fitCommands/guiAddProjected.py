import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from eos.saveddata.module import Module
from .calc.fitAddProjectedModule import FitAddProjectedModuleCommand
from logbook import Logger
import eos.db
pyfalog = Logger(__name__)


class GuiAddProjectedCommand(wx.Command):
    def __init__(self, fitID, id, type='item'):
        wx.Command.__init__(self, True, "Projected Add")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.id = id
        self.type = type

    def Do(self):
        result = False
        # since we can project various types, we need to switch of the fit command. We can't do this switch easily in
        # the fit command since each type might have a different kind of undo, easier to split it out
        if self.type == 'item':
            item = eos.db.getItem(self.id, eager=("attributes", "group.category"))

            if item.category.name == "Drone":
                # @todo: this may need to be reworked once we visit drone commands
                pyfalog.warn("DRONE PROJECTION NOT IMPLEMENTED")
                # drone = None
                # for d in fit.projectedDrones.find(item):
                #     if d is None or d.amountActive == d.amount or d.amount >= 5:
                #         drone = d
                #         break
                #
                # if drone is None:
                #     drone = Drone(item)
                #     fit.projectedDrones.append(drone)
                #
                # drone.amount += 1
            elif item.category.name == "Fighter":
                pyfalog.warn("FIGHTER PROJECTION NOT IMPLEMENTED")
                # fighter = Fighter(item)
                # fit.projectedFighters.append(fighter)
            elif item.group.name in Module.SYSTEM_GROUPS:
                pyfalog.warn("WH PROJECTION NOT IMPLEMENTED")
                # module = Module(item)
                # module.state = State.ONLINE
                # fit.projectedModules.append(module)
            else:
                # attempt a regular module projection
                result = self.internal_history.Submit(FitAddProjectedModuleCommand(self.fitID, self.id))
        elif self.type == 'fit':
            pyfalog.warn("FIT PROJECTION NOT IMPLEMENTED")

        if result:
            self.sFit.recalc(self.fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        self.sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
