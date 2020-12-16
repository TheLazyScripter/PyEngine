import copy
# __TODO: Fix this broken shit...

class PhysicsEngine(object):
    instance = None
    
    class Singleton(object):
        def __init__(self, objects):
            self.physics_objects = objects if objects else []
            self.gravity = None
    
        def add_object(self, game_object):
            assert game_object.get_component(CONSTANTS.COMPONENT_PHYSICS_RIGID_BODY2D)
            if not get_object_by_tag(game_object, self.physics_objects):
                self.physics_objects.append(game_object)
    
        def check_collision(self, game_object):
            col1 = game_object.get_component(CONSTANTS.COMPONENT_PHYSICS_BOX_COLLIDER2D)
            rb = game_object.get_component(CONSTANTS.COMPONENT_PHYSICS_RIGID_BODY2D)
            results = []
            if col1 and not col1.is_trigger:
                for i in self.physics_objects:
                    col2 = i.get_component(CONSTANTS.COMPONENT_PHYSICS_BOX_COLLIDER2D)
                    if col2 and not col2.is_trigger:
                        if (game_object.transform.position + rb.velocity).distance(i.transform.position) < .1:
                            results.append(i)
            return results
    
        @staticmethod
        def apply_force(game_object1, game_object2):
            rb1 = copy.deepcopy(game_object1.get_component(CONSTANTS.COMPONENT_PHYSICS_RIGID_BODY2D))
            rb2 = game_object2.get_component(CONSTANTS.COMPONENT_PHYSICS_RIGID_BODY2D)
    
            if not rb1.is_kinematic:
                game_object1.get_component(CONSTANTS.COMPONENT_PHYSICS_RIGID_BODY2D).apply_force(rb2)
    
            if not rb2.is_kinematic:
                rb2.apply_force(rb1)

        def start(self):
            for i in self.physics_objects:
                i.start()
    
        def update(self):
            for i in self.physics_objects:
                collisions = self.check_collision(i)
                for game_object in collisions:
                    self.apply_force(i, game_object)
    
                i.fixed_update()
                i.update()
    
    def __init__(self, objects=None):
        if not PhysicsEngine.instance:
            PhysicsEngine.instance = PhysicsEngine.Singleton(objects)
            
    def __getattr__(self, item):
        return getattr(PhysicsEngine.instance, item)
