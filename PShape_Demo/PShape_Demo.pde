PShape s;

void setup() {
  size(640, 360);
  noStroke();
  s = createShape();
}

void draw() {
    background(0);
    s.beginShape();
    s.fill(100);
    s.vertex(10,10);
    s.vertex(10,100);
    s.vertex(100, 100);
    s.vertex(100, 10);
    s.endShape(CLOSE);
    PVector v;
    v = new PVector((100 + (millis()/10)% 500), 100);
    //v = new PVector(random(100,600), random(100,300));
    //v = new PVector((mouseX>100)?mouseX:100 , (mouseY>100)?mouseY:100);
    s.setVertex(2, v);
    shape(s);
}
