from typing import List, Dict
import random

class CodeTemplateLibrary:
    """
    A class to store and manage reusable Java code templates for various programming tasks and patterns.
    """

    def __init__(self) -> None:
        """
        Initializes the CodeTemplateLibrary with a set of predefined Java code templates.
        """
        self.code_templates: Dict[str, str] = {
            "singleton": self._singleton_template(),
            "factory": self._factory_template(),
            "observer": self._observer_template(),
            "strategy": self._strategy_template(),
            "builder": self._builder_template(),
        }

    def get_templates(self) -> List[str]:
        """
        Retrieves a list of all code templates available in the library.

        Returns:
            List[str]: A list containing the names of the available code templates.
        """
        return list(self.code_templates.keys())

    def get_template(self, template_name: str) -> str:
        """
        Retrieves a specific code template by its name.

        Args:
            template_name (str): The name of the template to retrieve.

        Returns:
            str: The Java code template if found, else an error message.
        """
        return self.code_templates.get(template_name, "Template not found.")

    def _singleton_template(self) -> str:
        return (
            "public class Singleton {\n"
            "    private static Singleton instance;\n"
            "    private Singleton() {}\n"
            "    public static Singleton getInstance() {\n"
            "        if (instance == null) {\n"
            "            instance = new Singleton();\n"
            "        }\n"
            "        return instance;\n"
            "    }\n"
            "}"
        )

    def _factory_template(self) -> str:
        return (
            "public interface Product {\n"
            "    void use();\n"
            "}\n\n"
            "public class ConcreteProduct implements Product {\n"
            "    public void use() {\n"
            "        System.out.println(\"Using ConcreteProduct\");\n"
            "    }\n"
            "}\n\n"
            "public class Factory {\n"
            "    public static Product createProduct() {\n"
            "        return new ConcreteProduct();\n"
            "    }\n"
            "}"
        )

    def _observer_template(self) -> str:
        return (
            "import java.util.ArrayList;\n"
            "import java.util.List;\n\n"
            "public interface Observer {\n"
            "    void update(String message);\n"
            "}\n\n"
            "public class Subject {\n"
            "    private List<Observer> observers = new ArrayList<>();\n"
            "    public void addObserver(Observer observer) {\n"
            "        observers.add(observer);\n"
            "    }\n"
            "    public void notifyObservers(String message) {\n"
            "        for (Observer observer : observers) {\n"
            "            observer.update(message);\n"
            "        }\n"
            "    }\n"
            "}"
        )

    def _strategy_template(self) -> str:
        return (
            "public interface Strategy {\n"
            "    void execute();\n"
            "}\n\n"
            "public class ConcreteStrategyA implements Strategy {\n"
            "    public void execute() {\n"
            "        System.out.println(\"Executing Strategy A\");\n"
            "    }\n"
            "}\n\n"
            "public class Context {\n"
            "    private Strategy strategy;\n"
            "    public void setStrategy(Strategy strategy) {\n"
            "        this.strategy = strategy;\n"
            "    }\n"
            "    public void executeStrategy() {\n"
            "        strategy.execute();\n"
            "    }\n"
            "}"
        )

    def _builder_template(self) -> str:
        return (
            "public class Product {\n"
            "    private String partA;\n"
            "    private String partB;\n"
            "    public void setPartA(String partA) {\n"
            "        this.partA = partA;\n"
            "    }\n"
            "    public void setPartB(String partB) {\n"
            "        this.partB = partB;\n"
            "    }\n"
            "}\n\n"
            "public class Builder {\n"
            "    private Product product;\n"
            "    public Builder() {\n"
            "        product = new Product();\n"
            "    }\n"
            "    public Builder buildPartA(String partA) {\n"
            "        product.setPartA(partA);\n"
            "        return this;\n"
            "    }\n"
            "    public Builder buildPartB(String partB) {\n"
            "        product.setPartB(partB);\n"
            "        return this;\n"
            "    }\n"
            "    public Product build() {\n"
            "        return product;\n"
            "    }\n"
            "}"
        )

# Example of how to instantiate and use the CodeTemplateLibrary
if __name__ == "__main__":
    library = CodeTemplateLibrary()
    templates = library.get_templates()
    for template in templates:
        print(f"{template}:\n{library.get_template(template)}\n")