********************
Blinn Phong Material
********************

.. raw:: html

    <script>
    function setup() {
        let canvas = createCanvas(720, 400, WEBGL);
        canvas.parent('sketch-holder');
    }

    function draw() {
        background(205, 102, 94)
        rotateX(frameCount * 0.02)
        rotateY(frameCount * 0.01)
        locX = mouseX - width/2
        locY = mouseY - height/2
        specularColor(0, 0, 200)
        pointLight(255*0.8, 255, 255*0.8, locX, locY, 200)
        pointLight(255*0.7, 255, 255*0.7, locX, locY, 200)
        ambientLight(20, 50, 20)
        lightFalloff(1.3, 0, 0);
        specularMaterial(255, 255, 255)
        cone(100, 200)
    }
    </script>
    <div id="sketch-holder"></div>
    <br>


.. code:: python

    from p5 import *

    def setup():
        size(720, 400)

    def draw():
        background(205, 102, 94)
        rotate_x(frame_count * 0.02)
        rotate_y(frame_count * 0.01)
        blinn_phong_material()
        cone(200, 400)
        locX = mouse_x - width/2
        locY = mouse_y - height/2
        light_specular(0, 0, 255)
        point_light(360, 360*1.5, 360, locX, locY, 400)

    if __name__ == '__main__':
        run(mode='P3D')
