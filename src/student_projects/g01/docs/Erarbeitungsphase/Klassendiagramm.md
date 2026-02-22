```mermaid
classDiagram
direction LR

class FoxExpressView {
  +renderBacklog(orderCount:int) void
  +renderRoute(result:RouteResult) void
  +renderBenchmark(result:BenchmarkResult) void
  +showInfo(message:String) void
}

class FoxExpressController {
  -postOffice: PostOffice
  -routingService: RoutingService
  -benchmarkService: BenchmarkService
  -workloadContext: WorkloadContext
  +submitOrder(senderFox:String, recipient:String, startNode:String, targetNode:String) void
  +computeRouteFor(orderId:String) RouteResult
  +runBenchmark(startNode:String, targetNode:String, runs:int) BenchmarkResult
}

FoxExpressView --> FoxExpressController : UI events

class Animal {
  <<abstract>>
  +name:String
}

class Fox {
  +burrow:String
  +createOrder(recipient:Animal, startNode:String, targetNode:String) Delivery
  +submitTo(postOffice:PostOffice, order:Delivery) void
}

class FionaFuchs {
  +role:String = "Dispatcher"
  +decide(orderCount:int) void
}

Animal <|-- Fox

class Delivery {
  +id:String
  +sender:Animal
  +recipient:Animal
  +startNode:String
  +targetNode:String
  +status: DeliveryStatus
  +preference: DeliveryPreference
}

class DeliveryPreference {
  +handoverType:String
}
Delivery *-- DeliveryPreference

class PostOffice {
  -backlog: OrderBacklog
  +receive(order:Delivery) void
  +getCount() int
  +getById(orderId:String) Delivery
}

class OrderBacklog {
  -orders: List~Delivery~
  +add(order:Delivery) void
  +count() int
  +findById(orderId:String) Delivery
}

Fox --> Delivery : creates
Fox --> PostOffice : submits
PostOffice --> OrderBacklog : manages
OrderBacklog --> Delivery : stores *

class DeliveryStatus {
  <<interface>>
  +name() String
  +next() DeliveryStatus
}

class Received
class InTransit
class Delivered

DeliveryStatus <|.. Received
DeliveryStatus <|.. InTransit
DeliveryStatus <|.. Delivered
Delivery --> DeliveryStatus : status

class Graph {
  +nodes: List~String~
  +weights: Map~String,float~
}

class RouteResult {
  +path: List~String~
  +cost: float
  +timeMs: float
  +strategyName: String
}

class BenchmarkResult {
  +runs:int
  +meanMs: float
  +stdMs: float
  +strategyName: String
}

class IRoutingStrategy {
  <<interface>>
  +compute(graph:Graph, start:String, target:String) RouteResult
  +name() String
}

class CPythonRoutingStrategy
class PyPyRoutingStrategy
class NumbaRoutingStrategy

IRoutingStrategy <|.. CPythonRoutingStrategy
IRoutingStrategy <|.. PyPyRoutingStrategy
IRoutingStrategy <|.. NumbaRoutingStrategy
IRoutingStrategy --> Graph : uses

%% Factory Method (sichtbar & minimal)
class RoutingStrategyFactory {
  <<factory>>
  +createFor(orderCount:int) IRoutingStrategy
}

class WorkloadContext {
  -factory: RoutingStrategyFactory
  +update(orderCount:int) void
  +pickStrategy(orderCount:int) IRoutingStrategy
  +thresholds() String
}

class RoutingService {
  -workload: WorkloadContext
  +computeShortestPath(graph:Graph, start:String, target:String, orderCount:int) RouteResult
}

RoutingService --> WorkloadContext : reads
RoutingService ..> IRoutingStrategy : uses pickStrategy()
RoutingService --> RouteResult : returns

class BenchmarkService {
  +benchmark(graph:Graph, start:String, target:String, runs:int, strategy:IRoutingStrategy) BenchmarkResult
}

BenchmarkService ..> IRoutingStrategy : uses
BenchmarkService --> BenchmarkResult : returns

%% Story coupling
FionaFuchs ..> WorkloadContext : update(orderCount)

FoxExpressController --> PostOffice
FoxExpressController --> RoutingService
FoxExpressController --> BenchmarkService
FoxExpressController --> WorkloadContext : updates(orderCount)
FoxExpressController ..> FionaFuchs : story role
FoxExpressController ..> PostOffice : reads getCount()
