PShape s;

void setup() {
  size(640, 360);
  noStroke();
  s = createShape();
}

void draw() {
    background(0);
    fill(204);
    s.beginShape();
    s.vertex(10,10);
    s.vertex(10,100);
    s.vertex(100, 100);
    s.vertex(100, 10);
    s.endShape(CLOSE);
    PVector v;
    v = new PVector((100 + (millis()/10)% 500), 100);
    s.setVertex(2, v);
    shape(s);
//    s.setVertex(2, random_uniform(100,600), random_uniform(100,600));
//    s.setVertex(2, mouse_x if mouse_x>100 else 100, mouse_y if mouse_y>100 else 100);
}