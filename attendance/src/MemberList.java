import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.Optional;

public class MemberList {
    private List<Member> memberList;

    public MemberList() {
        this.memberList = new ArrayList<>();
    }

    public void addMember(Member member) {
        memberList.add(member);
    }

    public void readMemberList() {
        if (memberList.isEmpty()) {
            System.out.println("아직 멤버가 없습니다.");
        } else {
            for (Member member : memberList) {
                System.out.println(member);
            }
        }
    }

    public void updateMember(String name, Optional<String> newName, Optional<Integer> newGeneration, Optional<Part> newPart) {
        for (Member member : memberList) {
            if (member.getName().equals(name)) {
                newName.ifPresent(member::setName);
                newGeneration.ifPresent(member::setGeneration);
                newPart.ifPresent(member::setPart);
            }
        }
    }

    public void deleteMember(String name) {
        memberList.removeIf(member -> member.getName().equals(name));
    }

    public void printBackend() {
        List<Member> backendMembers = memberList.stream()
                .filter(member -> member.getPart() == Part.BACKEND)
                .collect(Collectors.toList());

        backendMembers.forEach(System.out::println);
    }

    public void generationAverage() {
        int sum = memberList.stream()
                .mapToInt(Member::getGeneration)
                .sum();

        double average = memberList.stream()
                .mapToInt(Member::getGeneration)
                .average()
                .orElse(0);

        System.out.println("평균 기수: " + average);
    }
}
