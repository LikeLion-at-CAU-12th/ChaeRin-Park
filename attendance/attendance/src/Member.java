public class Member {
    private String name;
    private int generation;
    private Part part;

    public Member(String name, int generation, Part part) {
        this.name = name;
        this.generation = generation;
        this.part = part;
    }

    String getName() {
        return name;
    }

    int getGeneration() {
        return generation;
    }

    Part getPart() {
        return part;
    }

    void setName(String name) {
        this.name = name;
    }

    void setGeneration(int generation) {
        this.generation = generation;
    }

    void setPart(Part part) {
        this.part = part;
    }

    @Override
    public String toString() {
        return "Member [name=" + name + ", generation=" + generation + ", part=" + part + "]";
    }
}
